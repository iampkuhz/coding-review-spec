---
name: java-review-spring-layering
description: 审查 Spring layering 与职责放置。适用于 controller、service、application service、transaction 或跨层数据流相关代码，尤其是 layered-service 或 MVC 项目。
---

# Java Spring Layering Review 指南

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-file --objective spring-layering --path <target-file>`。
2. 当变更以 adapter 或 controller 为中心时，使用 `SR-JAVA-MVC-CTRL-001`。
3. 如果问题本质上只是稳定的 package dependency 形状，则把 `DC-JAVA-SPRING-LAYER-001` 作为 routing hint，而不是 semantic finding。
4. 检查谁在持有 orchestration、transaction、validation handoff 与 transport mapping。

## 应该指出的问题

- business branching 或 transaction ownership 漂移到了 controller
- adapter-layer DTO 或 HTTP 概念泄漏到了 application behavior
- service 代码依赖了上层，或跳过了约定 boundary

## 不要指出的问题

- 纯 style 命名问题
- 本应迁移到 ArchUnit 的 package layout 评论
