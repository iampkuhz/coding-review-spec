# Harness 变更记录

## 2026-03-26 - 重构为标准 Harness Engineering 结构

### 变更内容
- 重构整个仓库为标准 Harness Engineering 结构
- 移动所有规则到 `.agent/rules-catalog/`
- 移动工具到 `.agent/hooks/`
- 移动配置到 `.agent/tool-profiles.json`
- 文档统一放到 `docs/agents/`

### 影响范围
- 所有文件路径变更
- 工具调用路径变更
