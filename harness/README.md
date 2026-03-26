# Harness Engineering - 代码审查执行器

## 概述

Harness Engineering 是代码审查的核心执行器，负责：
- 加载 harness.json 配置
- 调用 rule_tool.py 选择相关规则
- 组织 review 流程
- 输出结构化的审查结果

## 目录结构

```
harness/
├── harness.json                          # Harness 配置：定义审查流程、规则选择策略、skill 映射
├── review/                               # 代码审查执行器
│   ├── harness.py                        # 核心执行器：组织 review 流程
│   └── rule_tool.py                      # 规则工具：校验、选择、解释规则
└── rules/                                # 审查规约目录（核心资产）
    ├── catalog/                          # 规则分类目录
    │   ├── deterministic-candidate/      # 待迁移到工具的规则
    │   ├── governance-only/              # 仅用于治理的规则
    │   └── semantic/                     # 语义审查规则（LLM 处理）
    └── review-rule-schema.yaml           # 规则 Schema 定义
```

## 使用方式

### 1. 审查 git diff（最常用）

```bash
python3 harness/review/harness.py review-diff <target_repo_path> <dev_branch> <target_branch>
```

**示例：**
```bash
python3 harness/review/harness.py review-diff /Users/zhehan/my-project feature-branch main
```

### 2. 审查单个文件

```bash
python3 harness/review/harness.py review-file <target_repo_path> <file_path>
```

**示例：**
```bash
python3 harness/review/harness.py review-file /Users/zhehan/my-project src/main/java/com/example/OrderService.java
```

### 3. 审查整个 module 或 package

```bash
python3 harness/review/harness.py review-module <target_repo_path> <module_or_package>
```

**示例：**
```bash
python3 harness/review/harness.py review-module /Users/zhehan/my-project order-module
```

### 4. 架构审查

```bash
python3 harness/review/harness.py review-architecture <target_repo_path>
```

**示例：**
```bash
python3 harness/review/harness.py review-architecture /Users/zhehan/my-project
```

## 执行流程

### 标准执行过程（4 步）

#### 步骤 1: 选择相关规则
- 调用 `rule_tool.py select` 根据 scope、objective、path/module 选择规则
- 使用三层召回机制：
  - **第一层_精确匹配**：scope + objective + path/module 命中
  - **第二层_语义相关**：objective 或 path keyword 匹配
  - **第三层_兜底策略**：semantic-review 默认加载规则

#### 步骤 2: 加载专项 skill
- 根据命中的规则维度，从 `.qoder/skills/` 加载对应的 skill
- 技能映射关系在 `harness.json` 中定义

#### 步骤 3: 执行代码审查
- 使用选中的规则和 skill 分析代码
- 分离 semantic review 和 deterministic review

#### 步骤 4: 输出审查结果
- 结构化输出，包含：
  - 命中的规则 ID
  - 问题严重级别
  - checklist 检查结果
  - 具体修复建议

## harness.json 配置说明

### 核心配置项

```json
{
  "version": "1.0",
  "rule_catalog": "harness/rules/catalog",
  "cr_flows": {
    "review-diff": {
      "scope": "review-diff",
      "limit": 8
    }
  },
  "execution": {
    "rule_selection_strategy": "targeted",
    "minimum_score": 4
  },
  "skills": {
    "mapping": {
      "persistence": "java-review-persistence"
    }
  }
}
```

### 审查流程配置

- `review-diff`: 审查 git diff
- `review-file`: 审查单个文件
- `review-module`: 审查整个 module
- `review-architecture`: 架构审查

每个流程可配置：
- `scope`: 规则选择 scope
- `default_objective`: 默认审查目标
- `include_governance`: 是否包含 governance 规则
- `limit`: 最多选择的规则数

## 规则选择策略

### 评分机制

规则评分基于：
1. **scope 匹配** (+3 分)
2. **objective 匹配** (+3 分)
3. **path 匹配** (+2 分)
4. **module 匹配** (+2 分)
5. **semantic review 类别** (+1 分)

### 过滤策略

- 只选择 score >= minimum_score (默认 4) 的规则
- 如果有 targeted match，优先保留 targeted 规则
- 最多选择 limit 条规则 (默认 8 条)

## 与 OpenSpec 的关系

Harness Engineering 和 OpenSpec 是两个独立但互补的系统：

| 维度 | Harness Engineering | OpenSpec |
|------|---------------------|----------|
| **职责** | 代码审查执行器 | 规则治理流程 |
| **使用场景** | 对目标仓库执行 CR | 维护、更新 CR 规约 |
| **用户输入** | 待审查仓库路径、分支 | 规则提案、变更说明 |
| **自动化** | 全自动执行 | AI 生成审查文档，人工审核 |
| **产出** | 代码审查报告 | 规则准入/废弃决策 |

### 工作流程分离

#### Harness Engineering（代码审查）
```
用户提供：待审查仓库路径、开发分支、目标分支
    ↓
harness.py 自动加载配置
    ↓
rule_tool.py 选择相关规则
    ↓
加载对应 skill
    ↓
执行审查并输出结果
```

#### OpenSpec（规则治理）
```
用户提出：新规则建议
    ↓
AI 生成：rule-proposal.md
    ↓
AI 生成：rule-admission-review.md
    ↓
人工审核并决策
    ↓
更新 rules/catalog
```

## 本地工具使用

### 校验规则目录

```bash
python3 harness/review/rule_tool.py validate --strict
```

### 选择规则

```bash
python3 harness/review/rule_tool.py select \
  --scope review-diff \
  --objective persistence \
  --path src/main/java/com/example/OrderService.java
```

### 解释规则

```bash
python3 harness/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```

## 三层召回机制

Harness Engineering 使用三层召回机制确保规则覆盖：

### 第一层：精确匹配
- scope 完全匹配
- objective 关键词匹配
- path/module 精确命中

### 第二层：语义相关
- objective 语义扩展
- path keyword 匹配
- module 模式匹配

### 第三层：兜底策略
- semantic-review 规则默认加载
- 确保基础审查覆盖

## 输出格式

审查输出包含：

```
# 审查报告

## 命中的规则
- SR-JAVA-PERSISTENCE-001 | score=5 | Persistence boundary 检查
  摘要：确保 service 不直接持有 entity
  命中原因：scope=review-diff, path-keyword

## 审查发现
### [Major] Entity 泄漏到 service layer
- 问题：OrderService 直接持有 Order entity
- 建议：使用 DTO 进行数据传输
- 规则：SR-JAVA-PERSISTENCE-001

## Deterministic follow-up
- DC-JAVA-SPRING-LAYER-001: 建议迁移到 ArchUnit
```

## 最佳实践

1. **用户提供最少信息**：只需提供仓库路径和分支
2. **全自动执行**：harness 自动完成规则选择和审查
3. **结构化输出**：便于后续处理和分析
4. **规则覆盖保证**：三层召回机制确保无遗漏

## 故障排查

### 问题：没有匹配到规则
**解决：**
- 检查 scope 是否正确
- 尝试更宽的 objective
- 启用 `--include-governance`

### 问题：规则选择过多
**解决：**
- 降低 `limit` 参数
- 提高 `minimum_score` 配置
- 使用更具体的 objective

### 问题：规则选择过少
**解决：**
- 检查 path/module 是否正确
- 降低 `minimum_score` 配置
- 检查规则的 load_when 配置
