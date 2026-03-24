---
name: review-file
description: 基于与目标文件最相关的规则，审查单个文件或当前活动文件中的 Java / Spring / SOFA 代码。
---

执行一次 file-scope review。

把命令附加文本视为目标文件路径或文件线索；如果仍然不明确，再补一个简短澄清问题。

工作流：

1. 识别目标文件。
2. 运行 `python3 tools/review/rule_tool.py select --scope review-file --path <target-file>`。
3. 只读取被选中的 semantic rules，以及完成审查所需的最小周边代码。
4. 如果文件命中某个专门关注点，则使用对应 skill：
   - `java-review-mvc-controller-service`
   - `java-review-spring-layering`
   - `java-review-persistence`
   - `java-review-exception-semantics`
   - `java-review-sofa-boundary`
   - `java-review-domain-boundary`
5. 只报告从该文件及其直接依赖中能看见的 review finding。
6. 把 deterministic-candidate follow-up 与 semantic finding 分开展示。

输出顺序：

- Findings
- Deterministic routing suggestions
- Rules consulted
