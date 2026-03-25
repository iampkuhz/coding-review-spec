#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
RULE_DIR = ROOT / "rules" / "catalog"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "id",
    "title",
    "summary",
    "owner",
    "status",
    "category",
    "severity",
    "profile_tags",
    "applies_to",
    "review",
    "prompt_hints",
    "governance",
}

ALLOWED_STATUS = {"draft", "active", "deprecated", "rejected"}
ALLOWED_CATEGORY = {
    "semantic-review",
    "deterministic-candidate",
    "governance-only",
}
ALLOWED_SEVERITY = {"info", "minor", "major", "critical"}
CATEGORY_TO_ADMISSION = {
    "semantic-review": "keep-in-semantic-review",
    "deterministic-candidate": "migrate-to-deterministic",
    "governance-only": "reject-from-semantic-review",
}


def load_rule_files() -> tuple[list[dict[str, Any]], list[str]]:
    rules: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(RULE_DIR.rglob("*.yaml")):
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - defensive path
            errors.append(f"{path}: YAML 解析失败: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{path}: 顶层必须是 YAML object")
            continue
        payload["_path"] = path
        rules.append(payload)
    return rules, errors


def ensure(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_rule(rule: dict[str, Any], known_ids: set[str]) -> list[str]:
    errors: list[str] = []
    path = rule["_path"]
    missing = sorted(REQUIRED_TOP_LEVEL - rule.keys())
    if missing:
        errors.append(f"{path}: 缺少顶层字段: {', '.join(missing)}")
        return errors

    ensure(rule["schema_version"] == "v1", f"{path}: schema_version 必须是 v1", errors)
    ensure(rule["status"] in ALLOWED_STATUS, f"{path}: 非法 status {rule['status']}", errors)
    ensure(rule["category"] in ALLOWED_CATEGORY, f"{path}: 非法 category {rule['category']}", errors)
    ensure(rule["severity"] in ALLOWED_SEVERITY, f"{path}: 非法 severity {rule['severity']}", errors)
    ensure(isinstance(rule["profile_tags"], list), f"{path}: profile_tags 必须是 list", errors)

    applies_to = rule.get("applies_to", {})
    review = rule.get("review", {})
    prompt_hints = rule.get("prompt_hints", {})
    governance = rule.get("governance", {})
    deterministic = rule.get("deterministic", {})

    for field in ("languages", "frameworks", "paths"):
        ensure(
            isinstance(applies_to.get(field), list) and applies_to.get(field),
            f"{path}: applies_to.{field} 必须是非空 list",
            errors,
        )

    for field in ("objective", "comment_contract"):
        ensure(bool(review.get(field)), f"{path}: review.{field} 为必填项", errors)
    for field in ("checklist", "positive_indicators", "anti_patterns"):
        ensure(
            isinstance(review.get(field), list) and review.get(field),
            f"{path}: review.{field} 必须是非空 list",
            errors,
        )

    ensure(
        isinstance(prompt_hints.get("load_by_default"), bool),
        f"{path}: prompt_hints.load_by_default 必须是 boolean",
        errors,
    )
    load_when = prompt_hints.get("load_when", {})
    ensure(isinstance(load_when, dict), f"{path}: prompt_hints.load_when 必须是 object", errors)
    for field in ("scopes", "objectives"):
        ensure(
            isinstance(load_when.get(field), list),
            f"{path}: prompt_hints.load_when.{field} 必须是 list",
            errors,
        )

    admission = governance.get("admission_decision")
    expected_admission = CATEGORY_TO_ADMISSION.get(rule["category"])
    ensure(bool(admission), f"{path}: governance.admission_decision 为必填项", errors)
    ensure(
        admission == expected_admission,
        f"{path}: category {rule['category']} 必须使用 admission decision {expected_admission}",
        errors,
    )
    for field in ("rationale",):
        ensure(bool(governance.get(field)), f"{path}: governance.{field} 为必填项", errors)
    for field in ("evidence_required", "conflicts_with", "supersedes", "related_rules"):
        ensure(
            isinstance(governance.get(field), list),
            f"{path}: governance.{field} 必须是 list",
            errors,
        )

    if rule["category"] == "semantic-review":
        ensure(
            prompt_hints.get("load_by_default") or load_when.get("scopes"),
            f"{path}: semantic-review 规则必须声明 load strategy",
            errors,
        )
    else:
        ensure(
            not prompt_hints.get("load_by_default"),
            f"{path}: 只有 semantic-review 规则允许默认加载",
            errors,
        )

    if rule["category"] in {"deterministic-candidate", "governance-only"}:
        ensure(bool(deterministic.get("target_engine")), f"{path}: deterministic.target_engine 为必填项", errors)
        ensure(
            bool(deterministic.get("detection_strategy")),
            f"{path}: deterministic.detection_strategy 为必填项",
            errors,
        )

    reference_fields = ["conflicts_with", "supersedes", "related_rules"]
    for field in reference_fields:
        for ref_id in governance.get(field, []):
            if ref_id not in known_ids:
                errors.append(f"{path}: governance.{field} 引用了未知 rule id {ref_id}")

    return errors


def validate_catalog(strict: bool) -> int:
    rules, errors = load_rule_files()
    known_ids = {rule.get("id") for rule in rules if rule.get("id")}
    duplicate_counter = Counter(rule.get("id") for rule in rules if rule.get("id"))
    for rule_id, count in duplicate_counter.items():
        if count > 1:
            errors.append(f"检测到重复的 rule id: {rule_id}")
    for rule in rules:
        errors.extend(validate_rule(rule, known_ids))

    if strict:
        category_counts = Counter(rule.get("category") for rule in rules)
        for category in ALLOWED_CATEGORY:
            if category_counts.get(category, 0) == 0:
                errors.append(f"strict mode: category {category} 至少需要一条规则")

    if errors:
        print("Rule catalog 校验失败：")
        for item in errors:
            print(f"- {item}")
        return 1

    counts = Counter(rule["category"] for rule in rules)
    print(f"已成功校验 {len(rules)} 条 rule 文件。")
    for category in sorted(counts):
        print(f"- {category}: {counts[category]}")
    return 0


def path_matches(globs: list[str], candidate: str) -> bool:
    posix_path = candidate.replace("\\", "/").lstrip("./")
    pure = PurePosixPath(posix_path)
    return any(pure.match(pattern) or fnmatch.fnmatch(posix_path, pattern) for pattern in globs)


def text_matches(terms: list[str], haystack: str) -> bool:
    normalized = haystack.lower()
    return any(term.lower() in normalized for term in terms if term)


def extract_path_keywords(rule: dict[str, Any]) -> set[str]:
    applies_to = rule.get("applies_to", {})
    keywords: set[str] = set()
    for pattern in applies_to.get("package_patterns", []):
        keywords.update(token.lower() for token in re.findall(r"[A-Za-z0-9]+", pattern))
    for pattern in applies_to.get("paths", []):
        keywords.update(token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9]+", pattern))
    ignored = {
        "src",
        "main",
        "test",
        "java",
        "resources",
        "com",
        "org",
        "net",
        "api",
    }
    return {keyword for keyword in keywords if len(keyword) > 2 and keyword not in ignored}


def targeted_path_match(rule: dict[str, Any], paths: list[str]) -> tuple[bool, str | None]:
    if not paths:
        return False, None

    applies_to = rule.get("applies_to", {})
    globs = applies_to.get("paths", [])
    specific_globs = [pattern for pattern in globs if pattern not in {"**/*.java", "**/*", "*.java"}]
    for candidate in paths:
        if specific_globs and path_matches(specific_globs, candidate):
            return True, "path-specific"

    keywords = extract_path_keywords(rule)
    for candidate in paths:
        lowered = candidate.replace("\\", "/").lower()
        if any(keyword in lowered for keyword in keywords):
            return True, "path-keyword"

    return False, None


def score_rule(rule: dict[str, Any], scope: str, objective: str | None, paths: list[str], module: str | None) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    prompt_hints = rule.get("prompt_hints", {})
    load_when = prompt_hints.get("load_when", {})
    applies_to = rule.get("applies_to", {})

    if scope in load_when.get("scopes", []):
        score += 3
        reasons.append(f"scope={scope}")
    elif rule["category"] == "semantic-review" and prompt_hints.get("load_by_default"):
        score += 1
        reasons.append("semantic default")

    if objective:
        terms = [objective, *objective.split("-"), *objective.split("_")]
        search_space = " ".join(load_when.get("objectives", []) + rule.get("profile_tags", []))
        if text_matches(terms, search_space):
            score += 3
            reasons.append(f"objective={objective}")

    matched_path, match_reason = targeted_path_match(rule, paths)
    if matched_path and match_reason:
        score += 2
        reasons.append(match_reason)

    if module:
        for pattern in applies_to.get("module_patterns", []):
            if fnmatch.fnmatch(module, pattern):
                score += 2
                reasons.append(f"module={module}")
                break

    if rule["category"] == "semantic-review":
        score += 1

    return score, reasons


def select_rules(scope: str, objective: str | None, paths: list[str], module: str | None, include_governance: bool, limit: int) -> int:
    rules, errors = load_rule_files()
    if errors:
        print("无法加载 rule catalog：")
        for item in errors:
            print(f"- {item}")
        return 1

    selected: list[tuple[int, list[str], dict[str, Any]]] = []
    for rule in rules:
        if rule["category"] == "governance-only" and not include_governance:
            continue
        score, reasons = score_rule(rule, scope, objective, paths, module)
        if score > 0:
            selected.append((score, reasons, rule))

    selected.sort(key=lambda item: (-item[0], item[2]["category"], item[2]["id"]))
    if selected:
        def is_targeted(reasons: list[str]) -> bool:
            return any(reason not in {"semantic default"} and not reason.startswith("scope=") for reason in reasons)

        if (paths or module or objective) and any(is_targeted(reasons) for _, reasons, _ in selected):
            selected = [item for item in selected if is_targeted(item[1])]
        minimum_score = max(4, selected[0][0] - 2)
        selected = [item for item in selected if item[0] >= minimum_score]
    selected = selected[:limit]

    if not selected:
        print("没有匹配到目标规则。可以尝试更宽的 objective，或启用 governance 规则。")
        return 0

    print(f"# 已选择规则，scope={scope}")
    if objective:
        print(f"- objective: {objective}")
    if module:
        print(f"- module: {module}")
    if paths:
        print(f"- paths: {', '.join(paths)}")
    print()

    grouped: dict[str, list[tuple[int, list[str], dict[str, Any]]]] = {
        "semantic-review": [],
        "deterministic-candidate": [],
        "governance-only": [],
    }
    for item in selected:
        grouped[item[2]["category"]].append(item)

    for category in ("semantic-review", "deterministic-candidate", "governance-only"):
        items = grouped[category]
        if not items:
            continue
        print(f"## {category}")
        for score, reasons, rule in items:
            print(f"- {rule['id']} | score={score} | {rule['title']}")
            print(f"  摘要: {rule['summary']}")
            print(f"  命中原因: {', '.join(reasons)}")
            if category != "semantic-review":
                engine = rule.get("deterministic", {}).get("target_engine", "n/a")
                decision = rule.get("governance", {}).get("admission_decision", "n/a")
                print(f"  路由: {decision} via {engine}")
        print()

    return 0


def explain_rule(rule_id: str) -> int:
    rules, errors = load_rule_files()
    if errors:
        print("无法加载 rule catalog：")
        for item in errors:
            print(f"- {item}")
        return 1

    target = next((rule for rule in rules if rule.get("id") == rule_id), None)
    if not target:
        print(f"未找到规则: {rule_id}")
        return 1

    print(f"# {target['id']}")
    print(f"- 路径: {target['_path'].relative_to(ROOT)}")
    print(f"- 分类: {target['category']}")
    print(f"- 状态: {target['status']}")
    print(f"- Owner: {target['owner']}")
    print(f"- 严重级别: {target['severity']}")
    print(f"- 准入决策: {target['governance']['admission_decision']}")
    print(f"- 标题: {target['title']}")
    print()
    print(target["summary"])
    print()
    print("Checklist：")
    for item in target["review"]["checklist"]:
        print(f"- {item}")
    print()
    print("Anti-patterns：")
    for item in target["review"]["anti_patterns"]:
        print(f"- {item}")
    deterministic = target.get("deterministic")
    if deterministic:
        print()
        print("Deterministic routing：")
        print(f"- target engine: {deterministic.get('target_engine', 'n/a')}")
        if deterministic.get("suggested_artifact"):
            print(f"- suggested artifact: {deterministic['suggested_artifact']}")
        if deterministic.get("detection_strategy"):
            print(f"- detection strategy: {deterministic['detection_strategy']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Qoder review rule 本地工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="校验 rule catalog")
    validate_parser.add_argument("--strict", action="store_true", help="要求所有 category 都至少有规则覆盖")

    select_parser = subparsers.add_parser("select", help="为当前 review scope 选择规则")
    select_parser.add_argument("--scope", required=True, help="例如 review-diff、review-file、review-module、review-architecture、rule-add")
    select_parser.add_argument("--objective", help="按 review objective 收窄，例如 persistence 或 exception")
    select_parser.add_argument("--path", dest="paths", action="append", default=[], help="变更或被审查文件的路径")
    select_parser.add_argument("--module", help="module 名或 package 名")
    select_parser.add_argument("--include-governance", action="store_true", help="是否包含 governance-only 规则")
    select_parser.add_argument("--limit", type=int, default=8, help="最多输出多少条规则")

    explain_parser = subparsers.add_parser("explain", help="解释单条规则")
    explain_parser.add_argument("--rule", required=True, help="rule id")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "validate":
        return validate_catalog(strict=args.strict)
    if args.command == "select":
        return select_rules(
            scope=args.scope,
            objective=args.objective,
            paths=args.paths,
            module=args.module,
            include_governance=args.include_governance,
            limit=args.limit,
        )
    if args.command == "explain":
        return explain_rule(args.rule)
    parser.error(f"未知命令 {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
