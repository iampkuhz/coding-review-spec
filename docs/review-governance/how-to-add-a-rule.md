# 如何新增规则

## 什么时候应该加规则

只有当重复出现的 review 漏检或 review 不一致已经证明某个问题值得长期固化时，才新增规则。

## 工作流

1. 基于 `.openspec/templates/rule-proposal.md` 起草 `.openspec/changes/<date>-<slug>/proposal.md`。
2. 基于 `.openspec/templates/rule-admission-review.md` 起草 `.openspec/changes/<date>-<slug>/admission-review.md`。
3. 明确规则应属于哪一类：
   - `keep-in-semantic-review`
   - `migrate-to-deterministic`
   - `reject-from-semantic-review`
4. 把规则文件放入：
   - `.qoder/rules/catalog/semantic/`
   - `.qoder/rules/catalog/deterministic-candidate/`
   - `.qoder/rules/catalog/governance-only/`
5. 运行：

```bash
python3 tools/review/rule_tool.py validate --strict
```

6. 如果新规则替代旧规则，使用 `.openspec/templates/rule-deprecation.md` 记录，并更新 `supersedes`。

## Admission heuristics

- 需要 behavioral judgment 或 boundary judgment 的规则，保留在 semantic review。
- 主要描述稳定代码结构的规则，迁移到 deterministic tooling。
- 纯 style 或重复覆盖的规则，拒绝进入 semantic review。

## 好的规则 metadata 应包含

- `id`
- `owner`
- `status`
- `category`
- `profile_tags`
- `applies_to`
- `governance.conflicts_with`
- `governance.supersedes`
