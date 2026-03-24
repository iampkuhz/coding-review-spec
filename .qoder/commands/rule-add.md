---
name: rule-add
description: 新增或修改 Qoder review rule，并强制走 OpenSpec proposal 与 admission review 流程。
---

新增或修订一条规则。

不要仅凭直觉直接加规则，必须使用仓库中的治理资产。

工作流：

1. 读取：
   - `.qoder/rules/review-rule-schema.yaml`
   - `.openspec/templates/rule-proposal.md`
   - `.openspec/templates/rule-admission-review.md`
   - 如果本次变更涉及替代旧规则，还要读取 `.openspec/templates/rule-deprecation.md`
2. 在修改 catalog 前，先判断正确的 admission decision：
   - `keep-in-semantic-review`
   - `migrate-to-deterministic`
   - `reject-from-semantic-review`
3. 检查与现有规则的重叠关系：
   - 运行 `python3 tools/review/rule_tool.py validate --strict`
   - 运行 `python3 tools/review/rule_tool.py select --scope rule-add --objective governance --include-governance`
4. 在 `.openspec/changes/<date>-<slug>/` 下创建或更新 OpenSpec change record。
5. 只有当 admission rationale 明确后，才能把规则文件写入正确的 catalog category。
6. 重新运行 `python3 tools/review/rule_tool.py validate --strict`。
7. 总结：
   - 创建或修改了哪些文件
   - admission decision 是什么
   - 哪些范围被拒绝、冲突或 supersede

保持规则聚焦。如果一条规则更适合由 Checkstyle、PMD、ArchUnit 或其他 deterministic engine 执行，就把它路由过去，而不是塞进 semantic review prompt。
