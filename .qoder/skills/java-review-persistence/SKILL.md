---
name: java-review-persistence
description: 审查 repository、mapper、DAO 与 persistence boundary 语义。适用于涉及 repository、mapper、DAO、entity leakage 或 service-to-persistence contract 的 Java 代码。
---

# Java Persistence Review 指南

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-file --objective persistence --path <target-file>`。
2. 在评论前先阅读 `SR-JAVA-PERSISTENCE-001`。
3. 检查 repository API 是否保留了 domain 或 service 语义，以及 persistence 细节是否向上泄漏。
4. 如果问题只与 import 或 package dependency shape 有关，就把它路由到 deterministic tooling，而不是扩大 semantic review。

## 高价值 finding 的样子

- repository API 迫使 service 代码理解 mapper 或 ORM internals
- persistence entity 或 query wrapper 泄漏到了 service 或 RPC contract
- 由于 repository contract 过于 generic，partial update 语义变得模糊或不安全
