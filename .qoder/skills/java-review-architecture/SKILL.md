---
name: java-review-architecture
description: 审查 Java / Spring / SOFA 的 architecture seam、module boundary 与 rule routing。适用于检查 layer ownership、多 module boundary、dependency direction，以及判断某条规则应保留为 semantic review 还是迁移到 deterministic tooling。
---

# Java Architecture Review 指南

## 用途

当任务关注 architecture、dependency direction、boundary ownership，而不是单个文件的局部 style 时，使用这个 skill。

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-architecture`。
2. 如果问题集中在稳定 dependency direction 或 deterministic routing，再运行 `python3 tools/review/rule_tool.py select --scope review-architecture --objective architecture --include-governance`。
3. 只把命中的 semantic rule 放入当前推理。
4. 把 deterministic candidate 当作 routing hint，把 governance-only 规则当作 admission policy。
5. 检查 module entry point、adapter boundary、persistence seam、SOFA facade seam。
6. 优先输出能解释 maintainability 或 contract risk 的 finding，而不是命名偏好。

## Review 视角

- 职责是否落在正确的 boundary？
- dependency direction 是否保留了 transaction、contract、failure 的 ownership？
- 这个关注点应该继续保留在 semantic review，还是已经成熟到可以迁移到 ArchUnit、PMD、Checkstyle？
