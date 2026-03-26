# 代码审查规约管理指南

## 概述

本指南说明如何管理和维护代码审查规约。

## 规约分类

### Java / Spring / SOFA 审查规约

- `SR-JAVA-PERSISTENCE-001` - Repository 与 persistence boundary
- `SR-JAVA-DOMAIN-BOUNDARY-001` - DDD domain ownership
- `SR-JAVA-MVC-CTRL-001` - Controller 到 Service handoff
- `SR-JAVA-EXCEPTION-001` - Exception semantics
- `SR-JAVA-SOFA-BOUNDARY-001` - SOFA boundary
- `SR-JAVA-SPRING-LAYERING-001` - Spring layering

### Harness Engineering 审查规约

- `SR-HARNESS-ARCH-001` - AGENTS.md 全局入口
- `SR-HARNESS-AGENT-002` - .agentignore 文件访问控制
- `SR-HARNESS-DOCS-003` - docs/agents/ 分层文档
- `SR-HARNESS-CONFIG-004` - .agent/ 核心配置

## 规约管理流程

### 新增规约

1. 提出规约需求
2. 使用 `.openspec/templates/rule-proposal.md` 模板创建提案
3. 完成 admission review 流程
4. 添加到规约目录

### 修改规约

1. 说明修改原因
2. 更新对应的 YAML 文件
3. 运行校验工具验证

### 废弃规约

1. 说明废弃原因
2. 指定替代方案（如有）
3. 更新规约状态为 `deprecated`

## 规约目录结构

```
harness/rules/catalog/
├── semantic/                  # 语义审查规则（LLM 处理）
├── deterministic-candidate/   # 待迁移工具规则
└── governance-only/           # 治理规则
```

## 常用命令

### 校验规约目录

```bash
python3 harness/review/rule_tool.py validate --strict
```

### 查看规约详情

```bash
python3 harness/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```

### 选择规约

```bash
python3 harness/review/rule_tool.py select --scope review-diff --path src/main/java/com/example/OrderService.java
```

## 规约格式

每条规约包含：

- **基础信息**：id、title、summary、owner、status
- **适用范围**：languages、frameworks、paths
- **审查定义**：objective、checklist、anti-patterns
- **Prompt 提示**：load_by_default、load_when
- **治理信息**：admission_decision、related_rules

## 规约分类

### semantic-review
需要 LLM 语义理解的规约

### deterministic-candidate
可迁移到工具（ArchUnit、Checkstyle 等）的规约

### governance-only
仅用于治理的规约
