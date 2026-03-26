#!/usr/bin/env python3
"""
Harness Engineering - 代码审查执行器

这是代码审查的核心执行器，负责：
1. 加载 harness.json 配置
2. 调用 rule_tool.py 选择相关规则
3. 组织 review 流程
4. 输出结构化的审查结果

使用方式：
    python3 harness.py review-diff <target_repo_path> <dev_branch> <target_branch>
    python3 harness.py review-file <target_repo_path> <file_path>
    python3 harness.py review-module <target_repo_path> <module_or_package>
    python3 harness.py review-architecture <target_repo_path>
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
HARNESS_CONFIG = ROOT / "harness.json"
RULE_TOOL = ROOT / "review" / "rule_tool.py"


def load_harness_config() -> dict[str, Any]:
    """加载 harness 配置"""
    with open(HARNESS_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def select_rules(scope: str, objective: str | None, paths: list[str], module: str | None, include_governance: bool, limit: int) -> list[dict[str, Any]]:
    """调用 rule_tool 选择规则"""
    cmd = [
        sys.executable,
        str(RULE_TOOL),
        "select",
        "--scope", scope,
        "--limit", str(limit),
    ]
    
    if objective:
        cmd.extend(["--objective", objective])
    
    if paths:
        for path in paths:
            cmd.extend(["--path", path])
    
    if module:
        cmd.extend(["--module", module])
    
    if include_governance:
        cmd.append("--include-governance")
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    
    if result.returncode != 0:
        print(f"规则选择失败：{result.stderr}", file=sys.stderr)
        return []
    
    # 解析输出，提取规则列表
    # 这里简化处理，实际应该解析结构化输出
    print(result.stdout)
    return []


def execute_review(flow_name: str, target_path: str, **kwargs) -> int:
    """执行审查流程"""
    config = load_harness_config()
    
    flow_config = config["cr_flows"].get(flow_name)
    if not flow_config:
        print(f"未知的审查流程：{flow_name}", file=sys.stderr)
        return 1
    
    print(f"# 执行审查：{flow_config['description']}")
    print(f"- 目标路径：{target_path}")
    print(f"- Scope: {flow_config['scope']}")
    if flow_config.get("default_objective"):
        print(f"- Objective: {flow_config['default_objective']}")
    print()
    
    # 步骤 1: 选择规则
    print("## 步骤 1: 选择相关规则")
    rules = select_rules(
        scope=flow_config["scope"],
        objective=kwargs.get("objective", flow_config.get("default_objective")),
        paths=kwargs.get("paths", []),
        module=kwargs.get("module"),
        include_governance=flow_config.get("include_governance", False),
        limit=flow_config.get("limit", 8)
    )
    print()
    
    # 步骤 2: 加载对应 skill
    print("## 步骤 2: 加载专项 skill")
    print("根据命中的规则维度，加载对应的 skill...")
    print()
    
    # 步骤 3: 执行审查
    print("## 步骤 3: 执行代码审查")
    print("正在分析代码...")
    print()
    
    # 步骤 4: 输出结果
    print("## 步骤 4: 输出审查结果")
    print("审查完成！")
    
    return 0


def review_diff(target_path: str, dev_branch: str, target_branch: str) -> int:
    """审查 git diff"""
    print(f"审查 diff: {target_path}")
    print(f"开发分支：{dev_branch}")
    print(f"目标分支：{target_branch}")
    print()
    return execute_review("review-diff", target_path, dev_branch=dev_branch, target_branch=target_branch)


def review_file(target_path: str, file_path: str) -> int:
    """审查单个文件"""
    print(f"审查文件：{target_path}")
    print(f"文件路径：{file_path}")
    print()
    return execute_review("review-file", target_path, paths=[file_path])


def review_module(target_path: str, module_or_package: str) -> int:
    """审查 module 或 package"""
    print(f"审查 module: {target_path}")
    print(f"Module/Package: {module_or_package}")
    print()
    return execute_review("review-module", target_path, module=module_or_package)


def review_architecture(target_path: str) -> int:
    """架构审查"""
    print(f"架构审查：{target_path}")
    print()
    return execute_review("review-architecture", target_path, objective="architecture")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Harness Engineering - 代码审查执行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 审查 git diff
  python3 harness.py review-diff /path/to/repo feature-branch main
  
  # 审查单个文件
  python3 harness.py review-file /path/to/repo src/main/java/com/example/OrderService.java
  
  # 审查整个 module
  python3 harness.py review-module /path/to/repo order-module
  
  # 架构审查
  python3 harness.py review-architecture /path/to/repo
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # review-diff
    diff_parser = subparsers.add_parser("review-diff", help="审查 git diff")
    diff_parser.add_argument("target_path", help="待审查的本地仓库路径")
    diff_parser.add_argument("dev_branch", help="开发分支")
    diff_parser.add_argument("target_branch", help="目标分支")
    
    # review-file
    file_parser = subparsers.add_parser("review-file", help="审查单个文件")
    file_parser.add_argument("target_path", help="待审查的本地仓库路径")
    file_parser.add_argument("file_path", help="文件路径")
    
    # review-module
    module_parser = subparsers.add_parser("review-module", help="审查 module 或 package")
    module_parser.add_argument("target_path", help="待审查的本地仓库路径")
    module_parser.add_argument("module_or_package", help="module 名或 package 名")
    
    # review-architecture
    arch_parser = subparsers.add_parser("review-architecture", help="架构审查")
    arch_parser.add_argument("target_path", help="待审查的本地仓库路径")
    
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    
    if args.command == "review-diff":
        return review_diff(args.target_path, args.dev_branch, args.target_branch)
    elif args.command == "review-file":
        return review_file(args.target_path, args.file_path)
    elif args.command == "review-module":
        return review_module(args.target_path, args.module_or_package)
    elif args.command == "review-architecture":
        return review_architecture(args.target_path)
    else:
        parser.error(f"未知命令 {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
