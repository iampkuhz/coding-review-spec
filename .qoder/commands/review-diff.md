---
name: review-diff
description: 基于项目规则目录与聚焦 review skill，对当前 git diff 执行 Java / Spring / SOFA code review。
---

对当前仓库执行一次 diff-scope code review。

工作流：

1. 运行 `git status --short` 与 `git diff --name-only --diff-filter=ACMR`。
2. 把主分析范围限制在真正与 Java / Spring / SOFA review 相关的变更文件上。
3. 运行 `python3 tools/review/rule_tool.py select --scope review-diff --path <changed-file>...`。
4. 默认只把返回结果中的 `semantic-review` 规则放入主推理路径。
5. 把 `deterministic-candidate` 规则当作 routing hint：
   - 如果 diff 明显违反其意图，可在结果里指出
   - 不要把这些规则展开成大段 prompt context
   - 明确写出规则 metadata 中建议的 engine
6. 当 diff 命中以下关注点时，调用对应 skill：
   - controller 或 facade 流程：`java-review-mvc-controller-service`
   - service layering 与 architecture：`java-review-spring-layering`
   - repository、mapper、DAO、persistence contract：`java-review-persistence`
   - exception、rollback、error contract：`java-review-exception-semantics`
   - SOFA provider、consumer、facade boundary：`java-review-sofa-boundary`
   - DDD 风格 aggregate ownership：`java-review-domain-boundary`
7. 只输出具体的 correctness、semantic、boundary、contract 风险。
8. 输出顺序固定为：
   - Findings
   - Deterministic routing suggestions
   - Rules consulted

Review 风格：

- 优先输出精确的 reviewer-style comment，而不是泛泛总结。
- 每条 finding 都要绑定一个 rule id。
- 如果没有 semantic finding，要明确说明。
