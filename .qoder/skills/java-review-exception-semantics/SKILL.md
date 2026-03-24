---
name: java-review-exception-semantics
description: 审查 Java 与 Spring 的 exception semantics。适用于 exception type、catch block、rollback 行为、error mapping 或 SOFA/Spring caller-facing failure contract 变更。
---

# Java Exception Semantics Review 指南

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-file --objective exception --path <target-file>`。
2. 在评论前先阅读 `SR-JAVA-EXCEPTION-001`。
3. 聚焦丢失的 meaning、rollback intent、caller contract stability 与重复 logging。
4. 只有当 exception handling 改变了语义或可运维性时才评论，而不是因为 catch block 本身存在。

## 高信号问题

- 抛出的 exception 是否还能区分 business rejection 与 system failure？
- caller 现在看到的 contract 是否变得更不稳定或更不可操作？
- rollback 行为是否仍与最终抛出的 exception 对齐？
