---
name: review-module
description: 审查一个 Java module 或 package 子树，只加载与该范围相关的规则，而不是整个规则目录。
---

对某个 Java / Spring / SOFA module、service 或 package 子树执行 module-scope review。

把命令附加文本视为 module 名、顶层 package 或目录线索；必要时可检查仓库树来确认最接近的 module boundary。

工作流：

1. 解析当前要审查的 module、package 或目录。
2. 列出该 boundary 下的相关 source file。
3. 运行 `python3 tools/review/rule_tool.py select --scope review-module --module <module-name> --path <representative-file>...`。
4. 只加载命中的 semantic rule，把 deterministic candidate 单独保留。
5. 当出现 boundary hotspot 时，调用专用 skill：
   - `java-review-architecture`
   - `java-review-spring-layering`
   - `java-review-persistence`
   - `java-review-exception-semantics`
   - `java-review-sofa-boundary`
   - `java-review-domain-boundary`
6. 重点检查 module entry point、dependency direction、persistence leakage、RPC boundary、exception semantics。

输出顺序：

- Findings
- Deterministic routing suggestions
- Rules consulted
