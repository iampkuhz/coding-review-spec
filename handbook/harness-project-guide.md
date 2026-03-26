# Harness Engineering 项目审查指南

## 概述

本指南说明如何使用本规约仓库审查具有 Harness Engineering 结构的目标项目。

## Harness Engineering 项目特征

典型的 Harness Engineering 项目结构如下：

```
my-backend-project/
├── AGENTS.md                          # 【全局入口地图】
├── .agentignore                       # 【Agent 视野控制】
│
├── .agent/                            # 【Harness 核心配置目录】
│   ├── tool-profiles.json             # 工具权限与任务剖面
│   ├── plans/                         # 任务计划模板
│   ├── hooks/                         # 生命周期钩子脚本
│   ├── changelog.md                   # Harness 变更记录
│   └── metrics/                       # 质量度量
│
└── docs/
    └── agents/                        # 【模块级规范文档】
        ├── architecture.md            # 整体架构规则
        ├── backend.md                 # 后端专属规范
        ├── database.md                # 数据库操作规范
        └── testing.md                 # 测试规范
```

## 审查规则

本规约仓库包含以下针对 Harness Engineering 项目的审查规则：

### SR-HARNESS-ARCH-001 - AGENTS.md 全局入口
- **检查项**：项目根目录必须包含 AGENTS.md
- **要求**：包含项目概述、核心规则、指向 docs/agents/ 的索引
- **长度控制**：50-100 行以内

### SR-HARNESS-AGENT-002 - .agentignore 文件访问控制
- **检查项**：项目根目录必须包含 .agentignore
- **要求**：忽略敏感文件（.env）、基础设施目录（terraform/）

### SR-HARNESS-DOCS-003 - docs/agents/ 分层文档
- **检查项**：必须包含 docs/agents/ 目录
- **要求**：包含 architecture.md、backend.md 等分层文档

### SR-HARNESS-CONFIG-004 - .agent/ 核心配置
- **检查项**：必须包含 .agent/ 目录
- **要求**：包含 tool-profiles.json、plans/、hooks/ 等

## 使用方式

### 审查完整的 Harness 项目

```bash
python3 harness/review/harness.py review-module \
  /path/to/harness-project \
  harness-engineering
```

### 审查项目结构

```bash
python3 harness/review/rule_tool.py select \
  --scope review-architecture \
  --objective harness-engineering \
  --path /path/to/harness-project
```

### 解释 Harness 规则

```bash
python3 harness/review/rule_tool.py explain --rule SR-HARNESS-ARCH-001
```

## 审查重点

### 1. 项目结构完整性

- ✅ AGENTS.md 是否存在
- ✅ .agentignore 是否存在
- ✅ .agent/ 目录结构是否完整
- ✅ docs/agents/ 是否包含核心文档

### 2. 安全性检查

- ✅ .agentignore 是否忽略敏感文件
- ✅ tool-profiles.json 是否允许危险命令
- ✅ hooks 是否包含安全检查

### 3. 文档分层

- ✅ 文档是否分层组织
- ✅ AGENTS.md 是否指向详细文档
- ✅ 各层文档是否覆盖核心关注点

## 常见问题

### Q: 如何判断一个项目是否是 Harness Engineering 项目？

**A:** 检查是否包含以下特征文件：
- AGENTS.md
- .agentignore
- .agent/ 目录
- docs/agents/ 目录

### Q: 如果项目不符合 Harness 规范怎么办？

**A:** 审查报告会指出缺失的文件和目录，并提供修复建议。

### Q: 如何为特定技术栈（如 Java、TypeScript）定制 Harness 规则？

**A:** 可以在 docs/agents/backend.md 等技术栈专属文档中定义详细规范。

## 最佳实践

### 1. AGENTS.md 保持简洁

- 控制在 50-100 行
- 只包含核心 Golden Rules
- 详细规则放到 docs/agents/

### 2. .agentignore 覆盖全面

- 忽略 .env 等敏感文件
- 忽略 infrastructure/ 等基础设施目录
- 忽略生产部署脚本

### 3. .agent/ 配置安全

- tool-profiles.json 禁止危险命令
- hooks 包含 pre-commit 检查
- plans 定义标准流程

### 4. docs/agents/ 分层清晰

- architecture.md 定义整体架构
- backend.md 定义后端规范
- database.md 定义数据库操作
- testing.md 定义测试规范

## 示例项目

参考示例项目了解 Harness Engineering 的最佳实践：

```
my-backend-project/
├── AGENTS.md
├── .agentignore
├── .agent/
│   ├── tool-profiles.json
│   ├── plans/
│   │   ├── add-feature.yaml
│   │   ├── fix-bug.yaml
│   │   └── refactor.yaml
│   ├── hooks/
│   │   ├── pre-start.sh
│   │   ├── pre-commit.sh
│   │   └── post-failure.sh
│   └── changelog.md
└── docs/
    └── agents/
        ├── architecture.md
        ├── backend.md
        ├── database.md
        └── testing.md
```

## 总结

通过本指南，你应该能够：

✅ **识别 Harness Engineering 项目** - 检查特征文件和目录  
✅ **使用审查规则** - 应用 SR-HARNESS-*系列规则  
✅ **提供修复建议** - 指出缺失的文件和规范要求  
✅ **推广最佳实践** - 引导项目遵循 Harness Engineering 规范
