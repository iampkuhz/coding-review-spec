# OpenSpec 规则治理流程

## 概述

OpenSpec 负责代码审查规则的治理流程，包括：
- 新规则提案（rule-proposal）
- 规则准入审查（rule-admission-review）
- 规则冲突检查
- 规则替代或废弃记录

**注意**：OpenSpec 不是代码审查执行器，它只管理规则的增删改流程。

## 目录结构

```
harness/governance/openspec/
├── config.yaml                         # OpenSpec 配置
├── policies/
│   └── rule-admission-policy.md        # 规则准入标准
├── templates/
│   ├── rule-proposal.md                # 规则提案模板
│   ├── rule-admission-review.md        # 规则准入审查模板
│   └── rule-deprecation.md             # 规则废弃模板
└── changes/                            # 每次规则变更记录
    └── README.md                       # 变更记录索引
```

## 规则管理流程

### 流程 1：新增规则

#### 步骤 1: 提出规则（人工）
用户提出新规则需求，例如：
> "我们需要一个规则来检查 Controller 中是否直接调用了 DAO"

#### 步骤 2: 生成提案（AI 自动）
使用 `/rule-add` command，AI 自动生成：
- `.openspec/changes/<timestamp>-my-rule/rule-proposal.md`

**提案内容包含：**
- 规则 ID（建议）
- 规则标题和摘要
- 分类（semantic-review / deterministic-candidate / governance-only）
- 适用语言和框架
- review 维度和 checklist
- prompt hints（load_when 策略）

#### 步骤 3: 准入审查（AI 自动）
AI 自动生成：
- `.openspec/changes/<timestamp>-my-rule/rule-admission-review.md`

**审查内容：**
- 规则必要性分析
- 与现有规则的冲突检查
- 分类合理性评估
- 是否应该迁移到工具（deterministic）

#### 步骤 4: 人工决策（人工）
审查 rule-admission-review.md 的执行结果：
- ✅ **通过**：继续下一步
- ❌ **拒绝**：记录原因，结束流程
- 🔄 **需要修改**：返回步骤 2

#### 步骤 5: 创建规则文件（AI 自动）
根据提案创建规则 YAML 文件：
```bash
rules/catalog/semantic/sr-java-controller-dao.yaml
```

#### 步骤 6: 校验规则（AI 自动）
运行规则校验：
```bash
python3 harness/review/rule_tool.py validate --strict
```

#### 步骤 7: 记录变更（AI 自动）
更新 `changes/README.md` 索引

---

### 流程 2：修改规则

#### 步骤 1: 提出修改（人工）
用户提出修改需求，例如：
> "SR-JAVA-PERSISTENCE-001 的 checklist 需要增加一条关于 Repository 的要求"

#### 步骤 2: 生成变更提案（AI 自动）
AI 自动生成变更提案，说明：
- 修改的规则 ID
- 修改原因
- 修改内容对比

#### 步骤 3: 影响分析（AI 自动）
AI 分析修改影响：
- 是否影响现有审查结果
- 是否需要重新审查历史代码
- 是否与其他规则冲突

#### 步骤 4: 人工决策（人工）
审查变更提案和影响分析

#### 步骤 5: 更新规则文件（AI 自动）
修改对应的 YAML 文件

#### 步骤 6: 校验规则（AI 自动）
运行规则校验

---

### 流程 3：废弃规则

#### 步骤 1: 提出废弃（人工/AI）
提出废弃某规则，例如：
> "DC-JAVA-SPRING-LAYER-001 已经迁移到 ArchUnit，可以废弃了"

#### 步骤 2: 生成废弃记录（AI 自动）
AI 自动生成：
- `.openspec/changes/<timestamp>-deprecate-xxx/rule-deprecation.md`

**内容包括：**
- 废弃原因
- 替代规则（如果有）
- 迁移路径

#### 步骤 3: 人工决策（人工）
审查废弃记录

#### 步骤 4: 更新规则状态（AI 自动）
将规则 status 改为 `deprecated`

---

## 规则分类决策树

```
新规则提案
    ↓
是否需要业务语义理解？
    ├── 是 → semantic-review（LLM 处理）
    └── 否 → 继续判断
            ↓
    是否可以用工具检测？
        ├── 是 → deterministic-candidate（待迁移到工具）
        └── 否 → governance-only（仅用于治理）
```

### semantic-review
- 需要理解业务语义
- 需要判断设计合理性
- 需要上下文推理
- **示例**：Entity 泄漏、Boundary 模糊、职责错位

### deterministic-candidate
- 可以用工具检测（ArchUnit、Checkstyle 等）
- 规则明确、无歧义
- **示例**：Layer 依赖、命名规范、Import 顺序

### governance-only
- 不直接用于审查
- 用于记录治理决策
- 用于统计和审计
- **示例**：已废弃规则、风格指南

---

## 模板说明

### rule-proposal.md（规则提案）

```markdown
# 规则提案：{规则标题}

## 提案信息
- 建议 ID: {SR-XXX-001}
- 建议分类：{semantic-review | deterministic-candidate | governance-only}
- 建议 Owner: {团队/个人}

## 问题描述
为什么要增加这个规则？解决什么问题？

## 规则设计
### 分类
{分类及理由}

### 适用语言
- Java

### 适用框架
- Spring
- SOFA（如适用）

### 路径模式
- `**/controller/**`
- `**/service/**`

### Review 维度
#### 审查目标
{objective}

#### 检查清单
- [ ] 检查点 1
- [ ] 检查点 2

#### 正面模式
- 好的做法示例

#### 反面模式
- 常见错误示例

### Prompt Hints
#### 默认加载
{load_by_default: true/false}

#### 加载时机
- Scopes: [review-diff, review-module]
- Objectives: [persistence, exception]

## 治理决策
### 准入决策
{keep-in-semantic-review | migrate-to-deterministic | reject-from-semantic-review}

### 理由
{为什么这样决策}

### 证据
- 相关 issue
- 代码示例
```

### rule-admission-review.md（准入审查）

```markdown
# 规则准入审查：{规则 ID}

## AI 自动分析

### 必要性分析
✅ 必要 / ❌ 不必要

**理由：**
{AI 分析为什么必要}

### 分类合理性
✅ 合理 / ❌ 不合理

**当前分类：** {semantic-review | deterministic-candidate | governance-only}

**建议分类：** {建议}

**理由：**
{AI 分析分类是否合理}

### 冲突检查
✅ 无冲突 / ⚠️ 有冲突

**冲突规则：**
- {规则 ID 1}: {冲突说明}
- {规则 ID 2}: {冲突说明}

### 重叠检查
✅ 无重叠 / ⚠️ 有重叠

**重叠规则：**
- {规则 ID}: {重叠说明}

### 工具迁移可行性
✅ 可迁移 / ❌ 不可迁移

**建议工具：**
- ArchUnit（如适用）
- Checkstyle（如适用）
- 其他工具

**迁移路径：**
{如何迁移到工具}

## 审查结论
- [ ] 接受，保持当前分类
- [ ] 接受，调整分类为 {xxx}
- [ ] 拒绝，原因：{xxx}
- [ ] 需要进一步讨论

## 人工决策
审查人：{name}
决策：{接受/拒绝/修改}
日期：{YYYY-MM-DD}
```

### rule-deprecation.md（规则废弃）

```markdown
# 规则废弃：{规则 ID}

## 废弃原因
- [ ] 已迁移到工具（{工具名}）
- [ ] 规则过时，不再适用
- [ ] 与 {规则 ID} 重复/冲突
- [ ] 其他原因：{说明}

## 替代方案
- 替代规则：{规则 ID}（如适用）
- 替代工具：{工具名}（如适用）

## 迁移路径
如何从旧规则迁移到新规则/工具？

## 影响范围
- 影响的审查场景：{xxx}
- 需要重新审查的代码：{xxx}

## 审查结论
- [ ] 同意废弃
- [ ] 不同意废弃，理由：{xxx}

## 执行记录
执行日期：{YYYY-MM-DD}
执行人：{name}
```

---

## 与 Harness Engineering 的集成

OpenSpec 治理的规则最终会进入 `harness/rules/catalog`，供 Harness Engineering 使用。

### 数据流

```
OpenSpec 治理流程
    ↓
创建/更新规则 YAML
    ↓
存入 harness/rules/catalog
    ↓
Harness Engineering 加载规则
    ↓
执行代码审查
```

### 一致性保证

1. **规则校验**：每次规则变更后自动运行 `rule_tool.py validate`
2. **版本控制**：所有变更记录在 `changes/` 目录
3. **审计追踪**：每次变更都有提案、审查、决策记录

---

## 最佳实践

### 1. AI 自动化
- ✅ rule-proposal.md 应该由 AI 自动生成
- ✅ rule-admission-review.md 应该由 AI 自动生成
- ✅ 规则 YAML 文件应该由 AI 自动创建
- ✅ 规则校验应该由 AI 自动执行

### 2. 人工审核
- ✅ 人工审查 AI 生成的文档
- ✅ 人工做出最终决策
- ✅ 人工记录决策理由

### 3. 文档质量
- ✅ 提案必须清晰说明问题
- ✅ 审查必须包含冲突检查
- ✅ 废弃必须说明替代方案

---

## 常见问题

### Q: 为什么 rule-admission-review.md 要 AI 自动生成？
A: 因为 AI 可以：
- 自动检查与现有规则的冲突
- 自动分析分类合理性
- 自动评估工具迁移可行性
- 人工只需要审查 AI 的分析结果并做决策

### Q: 什么样的规则应该归类为 semantic-review？
A: 需要业务语义理解、设计合理性判断、上下文推理的规则。

### Q: 什么样的规则应该迁移到 deterministic-candidate？
A: 可以用工具（ArchUnit、Checkstyle 等）明确检测的规则。

### Q: 如何确保规则变更后审查的一致性？
A: 通过：
- 规则校验工具
- 变更记录文档
- 版本控制

---

## 工具使用

### 校验规则目录
```bash
python3 harness/review/rule_tool.py validate --strict
```

### 查看规则详情
```bash
python3 harness/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```

### 选择规则（测试）
```bash
python3 harness/review/rule_tool.py select \
  --scope review-diff \
  --objective persistence
```
