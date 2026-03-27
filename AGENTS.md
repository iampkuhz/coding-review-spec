# AGENTS.md - 代码审查规约仓库

## 项目概述

本仓库是 **Harness Engineering 规约仓库**，用于定义和管理代码审查规则。

## 架构描述

采用 Harness Engineering 标准结构：
- `.agent/` - 核心配置和规则目录
- `docs/agents/` - 分层规范文档

## 核心 Golden Rules

1. 所有审查规则必须存储在 `.agent/rules-catalog/`
2. 规则治理流程遵循 OpenSpec 规范
3. 文档分层：给人看的在 `docs/agents/`，给大模型看的也在 `docs/agents/`

## 目录索引

- [规约管理指南](docs/agents/governance-guide.md)
- [用户手册](docs/agents/user-manual.md)
- [Harness 项目审查指南](docs/agents/harness-project-guide.md)
