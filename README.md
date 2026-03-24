# coding-review-spec

这是一个面向 Java / Spring / SOFA 的项目级 Qoder code review 资产仓库。

当前仓库包含：

- `.qoder/rules/`：review rule schema 与 catalog，按 `semantic review`、`deterministic candidate`、`governance-only` 三类拆分
- `.qoder/commands/`：供 Qoder 直接调用的 review 与规则治理 commands
- `.qoder/skills/`：按关注点拆分的 Java review skills，而不是单一的大 prompt
- `.openspec/`：用于规则提案、准入、替代、废弃的 OpenSpec 治理模板
- `tools/review/rule_tool.py`：本地可运行的规则校验、选择、解释工具
- `docs/review-governance/`：使用与治理说明文档

快速验证：

```bash
python3 tools/review/rule_tool.py validate --strict
python3 tools/review/rule_tool.py select --scope review-diff --objective persistence --path src/main/java/com/example/order/OrderService.java
python3 tools/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```
