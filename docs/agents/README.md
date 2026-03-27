# OpenSpec 规则治理

这里的 OpenSpec 只承担 Qoder review rule 的治理层职责。

它不是主要的 review 执行器。真正执行 review 的是 Qoder commands、rules 与 skills。
OpenSpec 的职责是让规则变更流程显式、可审计。

## 负责内容

- 新规则 proposal
- 规则 admission review
- conflict 与 overlap 检查
- 规则 replacement 或 deprecation 记录

## 目录结构

- `config.yaml`：治理设置与 source-of-truth 路径
- `policies/rule-admission-policy.md`：规则准入标准
- `templates/`：proposal、admission、deprecation 模板
- `changes/`：由 `/rule-add` 创建的每次规则变更记录
