---
name: java-review-domain-boundary
description: 审查 DDD 风格的 domain ownership。适用于 aggregate、domain service、application service、invariant，或业务规则可能漂移到 adapter / repository 的场景。
---

# Java Domain Boundary Review 指南

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-file --objective domain --path <target-file>`。
2. 只有当 module 真的具备 DDD 风格职责时，才读取 `SR-JAVA-DOMAIN-BOUNDARY-001`。
3. 检查 invariant、state transition、business decision 现在由谁持有。
4. 如果 module 明显是普通 layered-service 代码，就退回使用 layering 与 persistence skill，而不要强套 DDD 术语。

## 应指出的问题

- repository、adapter 或 listener 变成了 domain decision 的真实 owner
- entity update 依赖 caller 自觉，而不是显式 domain operation
