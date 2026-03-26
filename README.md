# coding-review-spec

这是一个面向 Java / Spring / SOFA 的项目级 Qoder code review 资产仓库。

## 快速开始

### 使用代码审查助手

如果你想用这个仓库做自动 Java CR 助手，请参考：

- 📘 [**用户手册**](handbook/user-manual.md) - 如何发起审查、操作流程、完整示例
- 📗 [**规约管理指南**](handbook/governance-guide.md) - 如何管理和维护审查规约
- 📙 [**规则边界分析**](harness/governance/docs/review-governance/rule-boundary-analysis.md) - 哪些规则应该由工具处理，哪些应该由 LLM 处理

---

## 项目概述

当前仓库包含：

- `rules/`：审查规约目录（项目核心资产），按 `semantic review`、`deterministic candidate`、`governance-only` 三类拆分
- `.qoder/commands/`：供 Qoder 直接调用的 review 与规则治理 commands
- `.qoder/skills/`：按关注点拆分的 Java review skills，而不是单一的大 prompt
- `.openspec/`：用于规则提案、准入、替代、废弃的 OpenSpec 治理模板
- `harness/review/rule_tool.py`：本地可运行的规则校验、选择、解释工具
- `harness/governance/docs/review-governance/`：使用与治理说明文档（给大模型看）
- `handbook/`：用户手册和管理指南（给人看）

目录结构：

```text
.
├── rules/                                              # 审查规约目录（项目核心资产）
│   ├── catalog/                                        # 规则分类目录
│   │   ├── deterministic-candidate/                    # 待迁移到工具的规则（如 ArchUnit、Checkstyle）
│   │   │   └── dc-java-spring-layer-boundary.yaml      # 示例：Layer 依赖规则（应迁移到 ArchUnit）
│   │   ├── governance-only/                            # 仅用于治理的规则（不直接用于审查）
│   │   │   └── gv-style-import-order-reject.yaml       # 示例：Import 顺序规则（应迁移到 Checkstyle）
│   │   └── semantic/                                   # 语义审查规则（LLM 处理，需要业务理解）
│   │       ├── sr-java-domain-boundary.yaml            # DDD domain ownership 检查
│   │       ├── sr-java-exception-semantics.yaml        # 异常语义和 rollback 行为检查
│   │       ├── sr-java-mvc-controller-service.yaml     # Controller 到 Service handoff 质量检查
│   │       ├── sr-java-persistence-boundary.yaml       # Repository/persistence boundary 检查
│   │       ├── sr-java-sofa-boundary.yaml              # SOFA RPC boundary 检查
│   │       └── sr-java-spring-layering.yaml            # Spring layering 和职责放置检查
│   └── review-rule-schema.yaml                         # 规则 Schema 定义：YAML 文件的字段约束和验证规则
├── .openspec/                                          # OpenSpec 规则治理配置（点开头的隐藏目录，用于治理层流程）
│   ├── README.md                                       # OpenSpec 治理说明：规则变更流程、审计记录
│   ├── changes/                                        # 每次规则变更的记录（由 /rule-add 自动创建）
│   │   └── README.md                                   # 变更记录索引
│   ├── config.yaml                                     # OpenSpec 治理配置：模板路径、策略路径、工作流设置
│   ├── policies/                                       # 规则治理策略定义
│   │   └── rule-admission-policy.md                    # 规则准入标准：什么规则能被接受
│   └── templates/                                      # 规则治理文档模板
│       ├── rule-admission-review.md                    # 规则准入审查模板
│       ├── rule-deprecation.md                         # 规则废弃记录模板
│       └── rule-proposal.md                            # 规则提案模板
├── .qoder/                                             # Qoder 项目级资产（点开头的隐藏目录，Qoder 约定）
│   ├── commands/                                       # Qoder 命令定义：用户可调用的 review 和规则管理命令
│   │   ├── review-architecture.md                      # 命令：审查整体架构和 module boundary
│   │   ├── review-diff.md                              # 命令：审查 git diff（最常用）
│   │   ├── review-file.md                              # 命令：审查单个文件
│   │   ├── review-module.md                            # 命令：审查整个 module 或 package
│   │   ├── rule-add.md                                 # 命令：按治理流程新增或修改规则
│   │   ├── rule-explain.md                             # 命令：解释单条规则的详细内容
│   │   └── rule-validate.md                            # 命令：校验规则目录的完整性
│   └── skills/                                         # 审查技能：按关注点拆分的专项 review 指南
│       ├── java-review-architecture/                   # 技能：架构审查（module boundary、dependency direction）
│       │   └── SKILL.md                                # 技能定义文件
│       ├── java-review-domain-boundary/                # 技能：DDD domain ownership 审查
│       │   └── SKILL.md                                # 技能定义文件
│       ├── java-review-exception-semantics/            # 技能：异常语义审查
│       │   └── SKILL.md                                # 技能定义文件
│       ├── java-review-mvc-controller-service/         # 技能：MVC controller-service handoff 审查
│       │   └── SKILL.md                                # 技能定义文件
│       ├── java-review-persistence/                    # 技能：persistence boundary 审查
│       │   └── SKILL.md                                # 技能定义文件
│       ├── java-review-sofa-boundary/                  # 技能：SOFA boundary 审查
│       │   └── SKILL.md                                # 技能定义文件
│       └── java-review-spring-layering/                # 技能：Spring layering 审查
│           └── SKILL.md                                # 技能定义文件
├── handbook/                                           # 给人看的文档
│   ├── user-manual.md                                  # 用户手册
│   └── governance-guide.md                             # 规约管理指南
├── harness/                                            # Harness Engineering
│   ├── harness.json                                    # Harness 配置
│   ├── review/                                         # 代码审查执行器
│   │   ├── harness.py                                  # 核心执行器
│   │   └── rule_tool.py                                # 规则工具
│   ├── rules/                                          # 审查规约目录
│   └── governance/                                     # 规则治理层
│       ├── openspec/                                   # OpenSpec 配置
│       └── docs/                                       # 给大模型看的文档
├── tools/                                              # 本地工具脚本
│   └── review/                                         # 审查相关工具
│       ├── README.md                                   # 工具说明
│       └── rule_tool.py                                # 核心工具：校验、选择、解释规则（支持 validate/select/explain）
└── README.md                                           # 项目主文档（本文件）
```

## 文档导航

### 面向用户

- [**用户手册**](handbook/user-manual.md) - 如何发起审查、操作流程、完整示例
- [**规约管理指南**](handbook/governance-guide.md) - 如何管理和维护审查规约

### 面向规则治理

- [**规则边界分析**](harness/governance/docs/review-governance/rule-boundary-analysis.md) - 工具 vs LLM 的职责划分
- [**如何添加规则**](harness/governance/docs/review-governance/how-to-add-a-rule.md) - 规则提案和准入流程

---

## 目录命名说明

### 为什么使用 `.openspec/` 而不是 `openspec/`？

**原因：** `.openspec/` 只承担**规则治理层**的元数据管理，不是主要的 review 执行器。

- ✅ **治理流程元数据**：规则提案、准入审查、变更记录、废弃记录
- ✅ **需要隐藏**：这些是流程性文件，不应该干扰日常开发视线
- ✅ **审计导向**：保留规则演变历史，供后续追溯

真正的 review 执行是由 `.qoder/` 中的 commands、rules、skills 完成的。

**类比理解：**
- `.openspec/` = 公司的“规章制度档案室”（治理层，平时不看，需要时查阅）
- `.qoder/` = 公司的“实际操作手册”（执行层，每天都要用）

---

### 为什么使用 `.qoder/` 而不是 `qoder/`？

**原因：** 这是 Qoder 的**项目级资产约定**。

`.qoder/` 目录包含：
- **commands** - 用户可调用的命令（如 `/review-diff`）
- **rules** - 审查规则的 catalog（YAML 格式）
- **skills** - 按关注点拆分的专项 review 指南

这些都是**项目级配置**，不是源代码的一部分，因此放在隐藏目录中。

**对比：**
- `src/` - 你的业务代码（核心资产）
- `.qoder/` - Qoder 的审查资产（辅助工具）

---

## .qoder/ 文件的必要性分析

### ✅ 必须保留的文件

#### 1. `.qoder/commands/` - 7 个 command 文件
**用途：** 定义 Qoder 可调用的命令

| 文件 | 必要性 | 说明 |
|------|-------|------|
| `review-diff.md` | ✅ 核心 | 审查 git diff（最常用） |
| `review-file.md` | ✅ 核心 | 审查单个文件 |
| `review-module.md` | ✅ 核心 | 审查整个 module |
| `review-architecture.md` | ✅ 推荐 | 架构审查 |
| `rule-add.md` | ✅ 推荐 | 按治理流程添加规则 |
| `rule-explain.md` | ✅ 推荐 | 解释规则详情 |
| `rule-validate.md` | ✅ 推荐 | 校验规则目录 |

**结论：** 这些都是必要的，每个 command 对应一个 Qoder 功能入口。

---

#### 2. `.qoder/rules/` - 规则目录
**用途：** 存储所有审查规则

| 文件/目录 | 必要性 | 说明 |
|----------|-------|------|
| `review-rule-schema.yaml` | ✅ 核心 | 规则字段约束和验证 |
| `catalog/semantic/` | ✅ 核心 | 语义审查规则（LLM 处理） |
| `catalog/deterministic-candidate/` | ✅ 推荐 | 待迁移工具的规则 |
| `catalog/governance-only/` | ✅ 推荐 | 治理规则 |

**结论：** 这些都是必要的，规则是审查的核心资产。

---

#### 3. `.qoder/skills/` - 7 个 skill 文件
**用途：** 按关注点拆分的专项 review 指南

| Skill | 必要性 | 说明 |
|-------|-------|------|
| `java-review-persistence` | ✅ 核心 | persistence boundary 审查 |
| `java-review-mvc-controller-service` | ✅ 核心 | controller-service handoff |
| `java-review-exception-semantics` | ✅ 推荐 | 异常语义审查 |
| `java-review-spring-layering` | ✅ 推荐 | Spring layering 审查 |
| `java-review-sofa-boundary` | ✅ 推荐 | SOFA boundary 审查 |
| `java-review-domain-boundary` | ✅ 推荐 | DDD domain 审查 |
| `java-review-architecture` | ✅ 推荐 | 架构审查 |

**为什么需要拆分 skill 而不是一个大 prompt？**

1. **降低 token 消耗**：只加载相关的 skill，不是一次性加载所有
2. **聚焦审查**：每个 skill 专注一个关注点，避免泛泛而谈
3. **易于维护**：修改某个 skill 不影响其他

**结论：** 这些 skill 是必要的，但可以根据项目实际情况精简。

---

### ⚠️ 可以精简的文件

如果你的项目不需要某些审查维度，可以考虑移除对应的 skill：

**示例：如果你的项目不是 DDD 风格**
- 可以移除：`java-review-domain-boundary`

**示例：如果你的项目没有使用 SOFA**
- 可以移除：`java-review-sofa-boundary`

**示例：如果你只需要基本的 diff 审查**
- 保留：`review-diff.md` + `java-review-persistence` + `java-review-mvc-controller-service`
- 移除：其他 skill

---

### 📊 最小可用配置

如果你想要最小化配置，以下是**最小可用集合**：

```text
.qoder/
├── commands/
│   ├── review-diff.md              # 必须：diff 审查
│   └── rule-validate.md            # 必须：规则校验
├── rules/
│   ├── catalog/
│   │   └── semantic/
│   │       └── sr-java-persistence-boundary.yaml  # 必须：persistence 检查
│   └── review-rule-schema.yaml     # 必须：规则 schema
└── skills/
    └── java-review-persistence/    # 必须：persistence skill
        └── SKILL.md
```

**功能：** 可以执行基本的 persistence boundary 审查和规则校验。

---

### 📊 推荐配置（平衡）

对于大多数 Java / Spring 项目，推荐保留：

**Commands（3 个）：**
- `review-diff.md`
- `review-file.md`
- `rule-validate.md`

**Skills（3 个）：**
- `java-review-persistence`（最常见）
- `java-review-mvc-controller-service`（最常见）
- `java-review-spring-layering`（架构健康）

**Rules（3-5 条）：**
- `SR-JAVA-PERSISTENCE-001`
- `SR-JAVA-MVC-CTRL-001`
- `SR-JAVA-SPRING-LAYERING-001`
- （可选）`SR-JAVA-EXCEPTION-001`
- （可选）`DC-JAVA-SPRING-LAYER-001`

---

## 总结

### 目录命名

- ✅ `.openspec/` - 治理流程元数据（需要隐藏）
- ✅ `.qoder/` - Qoder 项目级资产（约定俗成）

### 文件必要性

- ✅ **Commands** - 7 个都是必要的（对应 Qoder 功能入口）
- ✅ **Rules** - 必须保留（审查的核心资产）
- ✅ **Skills** - 按项目需求精简（不是越多越好）

### 优化建议

1. **初期**：保留全部，充分使用
2. **中期**：根据实际使用情况，移除不常用的 skill
3. **长期**：推动 deterministic 规则迁移到本地工具（ArchUnit、Checkstyle 等）

核心原则：**让 LLM 聚焦在高价值的语义审查上，把能自动化的都自动化工具化。**

快速验证：

```bash
python3 harness/review/rule_tool.py validate --strict
python3 harness/review/rule_tool.py select --scope review-diff --objective persistence --path src/main/java/com/example/order/OrderService.java
python3 harness/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```
