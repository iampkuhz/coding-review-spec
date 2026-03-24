---
name: rule-validate
description: 校验 Qoder rule catalog、admission routing 与跨规则引用关系。
---

校验当前仓库中的 rule catalog。

工作流：

1. 运行 `python3 tools/review/rule_tool.py validate --strict`。
2. 如果校验失败，阅读具体文件并修复最小必要问题集。
3. 如果用户只要求校验报告，不要修改文件。
4. 输出结果时要区分：
   - schema shape 错误
   - category 与 admission decision 不匹配
   - 跨规则引用缺失
   - catalog coverage 缺口

如果治理上下文也重要，再补跑：

`python3 tools/review/rule_tool.py select --scope rule-validate --objective governance --include-governance`
