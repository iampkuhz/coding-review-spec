---
name: rule-explain
description: 解释一条规则，并说明它为什么属于 semantic、deterministic 或 governance-only。
---

解释当前仓库中的某一条规则。

把命令附加文本视为 rule id；如果没有给出 rule id，再询问一次。

工作流：

1. 运行 `python3 tools/review/rule_tool.py explain --rule <rule-id>`。
2. 只有在 explainer 输出还不够时，再去读原始 rule 文件。
3. 解释内容应包括：
   - 这条规则在检查什么
   - 它为什么属于当前 category
   - 它应该生成什么类型的 review comment，或不应该生成什么 comment
   - 它是否与其他规则冲突、supersede 其他规则，或把工作路由到 deterministic tooling

解释必须以仓库里的 metadata 为依据，而不是泛化的 code review 理论。
