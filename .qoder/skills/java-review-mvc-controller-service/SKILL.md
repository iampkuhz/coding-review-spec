---
name: java-review-mvc-controller-service
description: 审查 MVC 下 controller 到 service 的 handoff 质量。适用于 Spring controller、request mapping、transport DTO 处理或 controller orchestration 职责相关代码。
---

# Java MVC Controller-Service Review 指南

## 工作流

1. 运行 `python3 tools/review/rule_tool.py select --scope review-file --objective controller --path <target-file>`。
2. 阅读 `SR-JAVA-MVC-CTRL-001`。
3. 检查 controller 是否仍然只是 adapter，还是已经变成了隐藏的 service layer。
4. 每条 finding 都要绑定职责错位，而不是只说 method 太长。

## 强信号模式

- controller method 编排了多个 repository 或复杂业务分支
- transport-layer concern 与 domain decision 紧密耦合
- controller 中的 exception handling 改变了业务语义，而不是单纯做 contract mapping
