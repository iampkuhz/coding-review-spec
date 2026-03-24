# Review 治理说明

这个仓库现在包含一套项目级 Qoder review system，面向 Java / Spring / SOFA 代码库。

## 已实现内容

- `.qoder/commands/` 中的 Qoder commands
- `.qoder/skills/` 中的聚焦 Qoder skills
- `.qoder/rules/catalog/` 中的 typed review rule catalog
- `.openspec/` 中的 OpenSpec 治理模板
- `tools/review/rule_tool.py` 中的本地规则工具

## 核心设计

- semantic review rule 保持小而高信号
- deterministic candidate 从 prompt-heavy review 中分流出去
- governance-only rule 负责控制规则准入与拒绝
- command 会按当前 review scope 选择最小规则集

继续阅读：

- `how-to-run-review.md`
- `how-to-add-a-rule.md`
