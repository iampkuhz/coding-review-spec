# 规则准入审查

## Candidate

- Rule id:
- Rule title:
- Reviewer:
- Review date:

## Admission decision

- Decision:
  - `keep-in-semantic-review`
  - `migrate-to-deterministic`
  - `reject-from-semantic-review`

## 决策理由

为什么这条规则应该属于这个 category？

## Determinism 测试

- 这条规则能否表达为 package dependency、AST、naming、annotation 或 formatter logic？
- 如果可以，应该由哪个 engine 执行？
- 如果不可以，还剩下什么 semantic judgment 必须交给 Qoder review？

## Overlap 与 conflict 检查

- 已审查的相关规则：
- 是否发现 conflict：
- 是否需要 supersedes：

## Prompt budget 检查

- 这条规则是否会制造大范围低信号 prompt noise？
- 是否可以只在特定 scope 或 objective 下加载？

## 结论

- Approved:
- Merge 前必须补的修改：
- 后续 deterministic 工作项：
