# Rule 概念解析：上下文还是规约？

## 核心问题

> **Q:** 现在的场景，每条校验规则，都是一个 `.qoder/rule` 文件吗？有没有更好的办法？我以为 rule 更像是上下文，而不是执行过程中一个规约？

## 答案：Rule 既是上下文，也是规约

### Rule 的双重身份

**Rule 在仓库中有两种存在形式：**

1. **作为规约（Specification）** - 存储在 `.qoder/rules/catalog/` 目录下的 YAML 文件
2. **作为上下文（Context）** - 在审查过程中被 LLM 加载到 prompt 中

这两种身份并不矛盾，而是 Rule 在不同阶段的表现形式。

---

## Rule 的生命周期

### 阶段 1：规约定义（Specification）

**位置：** `.qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml`

```yaml
schema_version: v1
id: SR-JAVA-PERSISTENCE-001
title: Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节
summary: >
  Repository API 应保持 service-layer 语义，不应把 persistence entity、mapper DTO、
  framework-specific query object 或 partial update 语义泄漏到更高层。
review:
  objective: 保持面向 service 的 persistence contract 稳定
  checklist:
    - Repository 暴露的是具备 domain 含义的操作，而不是裸表操作或 mapper 细节。
    - Service 代码不依赖 persistence entity、query wrapper 或 mapper 的返回约定。
  anti_patterns:
    - Service 代码在 persistence boundary 之外直接操作 JPA entity 或 MyBatis record。
    - Repository method 从 service 接收 generic map、query wrapper 或 raw SQL fragment.
```

**这个阶段的 Rule 是：**
- ✅ **规约**：明确定义了什么是好的设计，什么是坏的设计
- ✅ **结构化数据**：以 YAML 格式存储，可被工具解析和校验
- ✅ **可治理**：有明确的生命周期（draft/active/deprecated）和准入流程

---

### 阶段 2：规则选择（Selection）

**执行：** `python3 tools/review/rule_tool.py select --scope review-diff --path OrderService.java`

**输出：**
```
## semantic-review
- SR-JAVA-PERSISTENCE-001 | score=6 | Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节
  命中原因：path-specific, semantic default
```

**这个阶段的 Rule 是：**
- ✅ **被筛选的规约**：根据当前审查范围，从所有规则中选出最相关的
- ✅ **带权重的上下文**：每条规则都有 score，用于排序和过滤

---

### 阶段 3：上下文加载（Context Loading）

**在 Qoder command 中：**

```markdown
# System Context

你将使用以下规则进行审查：

## Rule: SR-JAVA-PERSISTENCE-001

**目标：** 保持面向 service 的 persistence contract 稳定

**Checklist：**
1. Repository 暴露的是具备 domain 含义的操作，而不是裸表操作或 mapper 细节。
2. Service 代码不依赖 persistence entity、query wrapper 或 mapper 的返回约定。

**Anti-patterns：**
1. Service 代码在 persistence boundary 之外直接操作 JPA entity 或 MyBatis record.
2. Repository method 从 service 接收 generic map、query wrapper 或 raw SQL fragment.

**审查重点：**
- 只有当 persistence 细节泄漏到 service 行为或 public contract 时才提出 finding。
- 不要对纯 style 问题发表评论，除非它掩盖了真实的语义泄漏。
```

**这个阶段的 Rule 是：**
- ✅ **上下文**：被加载到 LLM 的 prompt 中，成为审查的"知识背景"
- ✅ **执行指南**：告诉 LLM 应该检查什么、忽略什么、如何评论

---

### 阶段 4：审查执行（Review Execution）

**LLM 的推理过程：**

```
思考：
1. 当前审查的文件是 OrderService.java
2. 加载的规则 SR-JAVA-PERSISTENCE-001 要求检查 persistence 语义泄漏
3. 检查 checklist：
   - ✅ Repository 方法返回的是 Order domain object，不是 MyBatis Record
   - ❌ 但是有一个方法接受了 Map<String, Object> 参数，这违反了规则
4. 查看 anti-patterns：
   - "Repository method 从 service 接收 generic map" - 正好匹配！
5. 生成审查意见，引用规则 ID
```

**输出：**
```markdown
### Finding

**问题：Repository 接受了 generic Map 参数**

- 位置：`OrderRepository.java:56`
- 违反规则：`SR-JAVA-PERSISTENCE-001`
- 问题描述：`findByCondition(Map<String, Object> params)` 方法接受了过于通用的参数...
```

**这个阶段的 Rule 是：**
- ✅ **判断标准**：LLM 根据规则的 checklist 和 anti-patterns 做判断
- ✅ **引用来源**：每条 finding 都绑定到具体的 rule id

---

## 为什么你会有"Rule 应该是上下文"的感觉？

### 你的直觉是对的

你说"rule 更像是上下文"，这个直觉非常准确！原因如下：

#### 1. Rule 不是"可执行代码"

Rule 文件（YAML）**不是**像 PMD/Checkstyle 那样的可执行脚本：

```java
// ❌ Rule 不是这样的
public class SR-JAVA-PERSISTENCE-001 {
    public void check(File file) {
        // 执行检查...
    }
}
```

```yaml
# ✅ Rule 实际是这样的
id: SR-JAVA-PERSISTENCE-001
checklist:
  - Repository 暴露的是具备 domain 含义的操作
  - Service 代码不依赖 persistence entity
```

**Rule 是知识，不是代码。** 它需要 LLM 来理解和执行。

#### 2. Rule 需要"解释执行"

LLM 执行 Rule 的过程是：

```
Rule (YAML) → LLM 理解 → 应用到具体代码 → 生成审查意见
```

这就像：
- **Rule = 法律条文**（规约）
- **LLM = 法官**（解释和执行）
- **代码 = 案件**（被审查对象）
- **审查意见 = 判决**（输出结果）

#### 3. Rule 的身份是"专家知识"

每条 Rule 实际上是一个**领域专家的知识片段**：

```yaml
# 这是一个专家的知识
id: SR-JAVA-PERSISTENCE-001
owner: review-governance@team  # 专家
checklist: [...]               # 专家的经验总结
anti_patterns: [...]           # 专家见过的反模式
```

当 LLM 加载这条 Rule 时，相当于**把专家的知识放入上下文**，用这个视角来审查代码。

---

## 更好的组织方式？

### 当前方式的优势

当前的设计（每条规则一个 YAML 文件）已经是很好的方式：

#### ✅ 优点 1：单一事实来源（Single Source of Truth）

```
.qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml
```

- 规则定义只有一份
- 修改后立即生效
- 不会出现多处不一致

#### ✅ 优点 2：可治理（Governable）

```yaml
governance:
  admission_decision: keep-in-semantic-review
  rationale: ...
  conflicts_with: [...]
  related_rules: [...]
```

- 每条规则有明确的治理信息
- 可以追踪规则之间的关系
- 可以审计规则的演变历史

#### ✅ 优点 3：可组合（Composable）

```bash
# 可以根据场景组合不同的规则
python3 tools/review/rule_tool.py select \
  --scope review-diff \
  --objective persistence
```

- 规则是独立的模块
- 可以按需加载
- 不会耦合在一起

---

### 可能的改进方向

#### 改进 1：Rule Profile（规则包）

当前问题：如果有很多条规则，如何快速加载一组相关的规则？

**解决方案：** 引入 Rule Profile

```yaml
# .qoder/rules/profiles/persistence-review.yaml
name: persistence-review
description: 专注于 persistence 边界的规则包
rules:
  - SR-JAVA-PERSISTENCE-001
  - SR-JAVA-DOMAIN-BOUNDARY-001
  - DC-JAVA-SPRING-LAYER-001
```

**使用方式：**
```bash
python3 tools/review/rule_tool.py select \
  --scope review-module \
  --profile persistence-review
```

---

#### 改进 2：Rule Chain（规则链）

当前问题：规则之间可能有依赖关系，如何表达？

**解决方案：** 引入 Rule Chain

```yaml
# .qoder/rules/chains/layered-service-chain.yaml
name: layered-service-chain
description: 分层服务架构的规则链
steps:
  - rule: SR-JAVA-MVC-CTRL-001      # 先检查 controller
    order: 1
  - rule: SR-JAVA-SPRING-LAYERING-001  # 再检查 service layering
    order: 2
  - rule: SR-JAVA-PERSISTENCE-001   # 最后检查 persistence boundary
    order: 3
```

**执行方式：**
```bash
python3 tools/review/rule_tool.py review \
  --scope review-module \
  --chain layered-service-chain
```

---

#### 改进 3：Rule Template（规则模板）

当前问题：相似的规则需要重复编写，如何复用？

**解决方案：** 引入 Rule Template

```yaml
# .qoder/rules/templates/boundary-check.yaml
# 这是一个模板，用于生成各种 boundary 检查规则
template:
  name: boundary-check
  parameters:
    - lower_layer
    - upper_layer
    - violation_type
  
  checklist_template:
    - "${upper_layer} 不应直接依赖 ${lower_layer} 的具体实现"
    - "${lower_layer} 的抽象不应泄漏到 ${upper_layer}"
  
  anti_pattern_template:
    - "${upper_layer} 代码直接 import ${lower_layer} 的具体类"
    - "${lower_layer} 的数据结构出现在 ${upper_layer} 的 public API"
```

**使用模板生成规则：**
```yaml
# .qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml
extends: boundary-check
parameters:
  lower_layer: persistence
  upper_layer: service
  violation_type: data-leakage
```

---

#### 改进 4：Rule as Context Annotation（规则上下文标注）

当前问题：LLM 在审查时，如何知道哪些规则已经应用了？

**解决方案：** 在审查过程中显式标注规则上下文

```markdown
## Review Session

**Loaded Rules:**
- ✅ SR-JAVA-PERSISTENCE-001 (active)
- ✅ SR-JAVA-MVC-CTRL-001 (active)
- ℹ️ DC-JAVA-SPRING-LAYER-001 (reference only)

**Review Context:**
当前审查 OrderService.java，这是一个 service layer 文件，主要关注：
1. Controller 到 Service 的 handoff（应用 SR-JAVA-MVC-CTRL-001）
2. Service 到 Repository 的调用（应用 SR-JAVA-PERSISTENCE-001）
3. Layer 依赖关系（参考 DC-JAVA-SPRING-LAYER-001）

---

## Findings

### Finding 1
- **Rule Applied:** SR-JAVA-PERSISTENCE-001
- **Context:** 检查 repository API 是否保留了 domain 含义
- **Finding:** Repository 方法接受了 generic Map 参数
```

这样 LLM 在审查过程中**始终保持对规则的感知**，不会忘记当前使用的是哪条规则。

---

## 关于"执行过程中不应该换 rule"的回应

### 你的理解是正确的

> "在执行过程中不论执行到了第几个规约的验证，都是这个身份，不应该换 rule。"

这个理解非常准确！在审查过程中：

#### ✅ 正确的做法

```
审查会话开始
  ↓
加载规则集合 {R1, R2, R3}
  ↓
对每个文件，用所有适用规则检查
  ↓
输出所有 findings（每条都标注 rule id）
  ↓
审查会话结束
```

**规则是审查的"知识背景"，不是"执行脚本"**。一旦加载，就全程可用，不会"用完就丢"。

#### ❌ 错误的理解

```
审查文件第 1 行 → 使用规则 R1
审查文件第 2 行 → 使用规则 R2  # 错误！规则不是这样切换的
审查文件第 3 行 → 使用规则 R3
```

---

### 实际的工作方式

在 Qoder 的 review command 中：

```markdown
# review-diff.md

工作流：

1. 运行 `git diff --name-only` 获取变更文件
2. 运行 `rule_tool.py select` 选择规则
   → 返回 [SR-JAVA-PERSISTENCE-001, SR-JAVA-MVC-CTRL-001, ...]
3. **把所有选中的规则加载到上下文**
4. 对每个变更文件，**用所有相关规则检查**
5. 输出时，**每条 finding 绑定到对应的 rule id**
```

**关键：** 规则是同时加载的，不是轮流使用的。LLM 会综合所有规则的视角来审查代码。

---

## 总结

### Rule 的本质

| 维度 | Rule 是什么 |
|------|-----------|
| **存储形式** | YAML 文件（规约） |
| **执行阶段** | LLM 的 prompt 上下文 |
| **作用** | 专家知识的载体 |
| **生命周期** | draft → active → deprecated |
| **治理** | 有准入、冲突检查、替代关系 |

### Rule 的使用方式

```
规约定义 (YAML)
    ↓
规则选择 (select)
    ↓
上下文加载 (prompt)
    ↓
LLM 理解执行
    ↓
审查意见输出
```

### 关于你的疑问

✅ **你说得对**：Rule 更像是上下文  
✅ **补充一点**：它首先是规约，然后在执行时转化为上下文  
✅ **你的直觉**：执行过程中不应该换 rule → 完全正确！

### 更好的组织方式？

当前方式已经很好：
- ✅ 每条规则一个 YAML 文件
- ✅ 按 category 分类管理
- ✅ 通过 `select` 智能加载

可能的改进：
- Rule Profile（规则包）
- Rule Chain（规则链）
- Rule Template（规则模板）
- Context Annotation（上下文标注）

但这些都需要根据实际需求来决定是否引入，避免过度设计。

**核心原则：** Rule 是结构化的专家知识，既是规约也是上下文，两者并不矛盾。
