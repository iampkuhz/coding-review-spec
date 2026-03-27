# 规则准入策略

## 目的

让 semantic review 只关注高信号的 correctness、boundary 与 contract 问题。

## Admission decision

### `keep-in-semantic-review`

当一条规则需要 behavioral judgment 或 boundary judgment，无法稳健地下沉为 deterministic checker 时，使用这个 decision。

典型例子：

- controller responsibility placement
- persistence model 向 service 或 RPC contract 泄漏
- exception meaning 与 rollback semantics
- SOFA contract stability

### `migrate-to-deterministic`

当一条规则主要描述稳定的 package、dependency、naming、annotation、AST 模式时，应该迁移到 ArchUnit、PMD、Checkstyle 或小型 script。

典型例子：

- package dependency direction
- forbidden import
- annotation presence rule
- naming 或 formatting requirement

### `reject-from-semantic-review`

当一条规则几乎不提供 semantic 价值，只会增加 review noise 时，应直接拒绝进入 semantic review。

典型例子：

- import ordering
- blank line 或 brace placement
- 纯 style 的 naming consistency

## Mandatory check

在激活规则前，必须完成：

1. 检查现有规则是否已经覆盖该问题。
2. 记录 `conflicts_with`、`supersedes`、`related_rules`。
3. 明确正确的 admission class。
4. 运行 `python3 tools/review/rule_tool.py validate --strict`。

## Rejection criteria

当出现以下情况时，应拒绝一条 semantic rule：

- 它是纯 style 问题
- 它完全可由 deterministic tooling 覆盖
- 它与已有规则重复，但没有缩小适用范围
- 它没有说明适用边界
