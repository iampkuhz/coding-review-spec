# 如何运行 Review

## Qoder commands

在 Qoder 中使用这些项目级 command：

- `/review-diff`：审查当前 git diff
- `/review-file <path>`：审查单个文件
- `/review-module <module-or-package>`：审查一个 module 或 package 子树
- `/review-architecture`：检查 architecture 与 module boundary
- `/rule-add`：按治理流程新增或修改规则
- `/rule-validate`：校验 rule catalog
- `/rule-explain <RULE-ID>`：解释某条规则

## 这些 command 会做什么

- 调用 `tools/review/rule_tool.py` 选择最相关的规则
- 把 semantic rule 与 deterministic rule 分开处理
- 只有在代码确实命中某个维度时，才调用对应的聚焦 skill

## 常用本地检查

```bash
python3 tools/review/rule_tool.py validate --strict
python3 tools/review/rule_tool.py select --scope review-diff --path src/main/java/com/example/OrderController.java
python3 tools/review/rule_tool.py explain --rule SR-JAVA-EXCEPTION-001
```

## 理想的 review 输出

好的 review 输出应该：

- 引用对应的 rule id
- 解释 semantic 或 boundary 风险
- 给出具体修复建议
- 把 deterministic follow-up suggestion 与 semantic finding 分开
