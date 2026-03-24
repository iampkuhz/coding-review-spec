# Qoder Review Rules 说明

这个目录是 Qoder 的项目级 review rule catalog。

## 目标

- 保持 `semantic review` 规则小而明确，便于长期维护。
- 对适合 ArchUnit、Checkstyle、PMD 的规则做 deterministic routing，避免挤占 prompt 预算。
- 为每一次新增规则、修改规则、废弃规则保留可追溯的治理记录。

## 目录结构

- `review-rule-schema.yaml`：`tools/review/rule_tool.py` 使用的 metadata contract
- `catalog/semantic/`：应进入 LLM-driven semantic review 的规则
- `catalog/deterministic-candidate/`：通常应迁移到 static tooling 的规则
- `catalog/governance-only/`：只用于准入、拒绝、catalog policy 的治理规则

## 运行方式

1. Qoder commands 先通过 `python3 tools/review/rule_tool.py select ...` 选择小范围规则。
2. 默认只把 `semantic-review` 规则放入主 review reasoning。
3. `deterministic-candidate` 只作为 routing hint，不作为 prompt 负担。
4. `governance-only` 规则只负责控制哪些规则能进入或离开 catalog。

## Rule 生命周期

1. 使用 `.openspec/templates/rule-proposal.md` 起草 proposal。
2. 使用 `.openspec/templates/rule-admission-review.md` 完成 admission review。
3. 新增或更新 catalog entry。
4. 运行 `python3 tools/review/rule_tool.py validate --strict`。
5. 当规则被替代或废弃时，用 `.openspec/templates/rule-deprecation.md` 记录。
