---
name: review-architecture
description: 检查 Java / Spring / SOFA 服务的 architecture boundary、module seam 与 rule routing。
---

执行一次 architecture-focused review。

这个 command 关注 boundary 质量、ownership 与 rule routing，不做 style 或逐行吹毛求疵。

工作流：

1. 检查与请求相关的仓库结构或 module 结构。
2. 运行 `python3 tools/review/rule_tool.py select --scope review-architecture`。
3. 当问题聚焦于稳定 dependency direction 或 deterministic routing 时，再运行 `python3 tools/review/rule_tool.py select --scope review-architecture --objective architecture --include-governance`。
4. 读取命中的规则，并以 `java-review-architecture` 作为主 skill。
5. 对 hotspot 再叠加 persistence、exception semantics、SOFA boundary、DDD boundary 等专用 skill。
6. 明确区分：
   - semantic review finding
   - 应迁移到 ArchUnit、Checkstyle、PMD 的 deterministic candidate
   - 关于某条规则是否应进入 catalog 的 governance note
7. 优先输出那些能解释 boundary 为什么影响 maintainability、transaction ownership、contract stability、failure isolation 的 finding。

输出顺序：

- Architecture findings
- Deterministic routing suggestions
- Governance notes
- Rules consulted
