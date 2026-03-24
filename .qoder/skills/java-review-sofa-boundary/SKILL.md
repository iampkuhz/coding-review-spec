---
name: java-review-sofa-boundary
description: 审查 SOFA provider、consumer 与 facade boundary。适用于 RPC DTO、facade interface、provider adapter、consumer、跨 module contract 或 remote error handling 相关代码。
---

# Java SOFA Boundary Review 指南

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-file --objective sofa --path <target-file>`。
2. 阅读 `SR-JAVA-SOFA-BOUNDARY-001`，必要时再叠加相关 exception rule。
3. 检查 facade DTO、返回 contract 与 remote error 是否在跨 module boundary 上保持稳定。
4. 优先输出关于 compatibility、contract leakage、error ownership 的评论。

## 重点识别模式

- 内部 entity 或 persistence model 被直接暴露为 RPC contract
- provider-specific exception 泄漏穿过 facade interface
- consumer 的分支逻辑依赖 provider implementation detail
