# Java 代码审查助手 - 用户操作手册

## 快速开始

### 基本用法

当你需要对 Java 项目进行代码审查时，只需提供以下信息：

```
请你帮我做代码 CR：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：xiangbin/wcctp_optimization
- 目标分支：master
- 审查范围：[可选] 特定文件、模块或全量 diff
- 审查重点：[可选] 例如 persistence、exception、architecture 等
```

### 示例

**示例 1：审查完整的 PR diff**
```
请你帮我做代码 CR：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：feature/order-optimization
- 目标分支：master
- 审查范围：全量 diff
```

**示例 2：审查特定模块**
```
请你帮我做代码 CR：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：feature/order-optimization
- 目标分支：master
- 审查范围：order-module 子树
- 审查重点：persistence boundary
```

**示例 3：审查特定文件**
```
请你帮我做代码 CR：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：feature/order-optimization
- 目标分支：master
- 审查范围：src/main/java/com/example/order/OrderService.java
```

---

## 完整操作流程

### 阶段 1：用户输入（手工操作）

#### 步骤 1.1：准备审查请求

**用户需要提供：**

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 仓库路径 | ✅ | 目标 git 仓库的本地绝对路径 | `/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis` |
| 开发分支 | ✅ | 包含变更的特性分支 | `feature/order-optimization` |
| 目标分支 | ✅ | 合并目标分支（通常是 master/develop） | `master` |
| 审查范围 | ❌ | 默认为全量 diff，可指定文件/模块 | `src/main/java/com/example/order/` |
| 审查重点 | ❌ | 指定特定关注点，如 persistence、exception | `persistence` |

#### 步骤 1.2：切换到目标仓库

```bash
cd /Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
git checkout xiangbin/wcctp_optimization
git pull origin xiangbin/wcctp_optimization
```

#### 步骤 1.3：确认变更范围

```bash
# 查看变更文件列表
git diff --name-only master..xiangbin/wcctp_optimization

# 查看变更统计
git diff --stat master..xiangbin/wcctp_optimization
```

---

### 阶段 2：Spec 自动执行（LLM 自动处理）

#### 步骤 2.1：加载审查规则

**LLM 自动执行：**

1. 读取本仓库的规则目录：
   ```
   .qoder/rules/catalog/
   ├── semantic/           # 语义审查规则（LLM 处理）
   ├── deterministic-candidate/  # 待迁移工具规则
   └── governance-only/    # 治理规则
   ```

2. 运行规则选择工具：
   ```bash
   python3 /Users/zhehan/Documents/tools/llm/openspec/coding-review-spec/tools/review/rule_tool.py select \
     --scope review-diff \
     --path <变更文件列表> \
     --objective <审查重点（如有）>
   ```

3. 根据返回结果，只加载 `semantic-review` 类别的规则到上下文中。

#### 步骤 2.2：分析代码变更

**LLM 自动执行：**

1. 读取变更文件的完整内容（不仅是 diff）
2. 结合选中的审查规则，逐条检查代码
3. 对每个关注点调用对应的 skill：
   - 涉及 controller/service → `java-review-mvc-controller-service`
   - 涉及 repository/DAO → `java-review-persistence`
   - 涉及 exception → `java-review-exception-semantics`
   - 涉及 SOFA → `java-review-sofa-boundary`
   - 涉及 architecture → `java-review-architecture`

#### 步骤 2.3：生成审查意见

**LLM 自动执行：**

按以下固定格式输出审查结果：

```markdown
## Code Review 结果

### 审查范围
- 仓库：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 分支：xiangbin/wcctp_optimization → master
- 变更文件：12 个
- 应用规则：SR-JAVA-PERSISTENCE-001, SR-JAVA-MVC-CTRL-001, ...

---

### Findings（按严重级别排序）

#### 🔴 Critical

**问题 1：[简短标题]**
- 位置：`src/main/java/.../OrderService.java:45`
- 违反规则：`SR-JAVA-PERSISTENCE-001`
- 问题描述：Repository API 泄漏了 MyBatis 的 Record 对象到 service layer
- 修复建议：...

#### 🟡 Major

**问题 2：[简短标题]**
- 位置：`src/main/java/.../OrderController.java:78`
- 违反规则：`SR-JAVA-MVC-CTRL-001`
- 问题描述：Controller 直接返回了 persistence entity
- 修复建议：...

---

### Deterministic Routing Suggestions

以下问题建议通过本地工具检查（不在 LLM 审查范围）：

1. **Layer 依赖违规**
   - 位置：`OrderController.java`
   - 建议工具：ArchUnit
   - 参考规则：`DC-JAVA-SPRING-LAYER-001`

2. **Import 顺序问题**
   - 位置：多个文件
   - 建议工具：Checkstyle
   - 参考规则：`GV-STYLE-IMPORT-001`

---

### Rules Consulted

本次审查应用的规则：
- ✅ SR-JAVA-PERSISTENCE-001 - Repository 与 persistence boundary
- ✅ SR-JAVA-MVC-CTRL-001 - Controller 到 Service handoff
- ℹ️ DC-JAVA-SPRING-LAYER-001 - Layer 依赖（仅 routing hint）
```

---

### 阶段 3：用户确认与修复（手工操作）

#### 步骤 3.1：审查结果确认

**用户需要：**

1. 阅读 LLM 输出的审查意见
2. 判断每个 finding 是否合理
3. 对于不确定的建议，可以追问：
   ```
   关于问题 1，为什么 Repository 不应该暴露 MyBatis Record？
   ```

#### 步骤 3.2：执行修复

**用户需要：**

1. 根据审查意见修复代码
2. 对于 deterministic routing suggestions，推动团队在本地工具中配置：
   ```bash
   # 例如添加 ArchUnit 测试
   src/test/java/com/example/LayerDependencyArchTest.java
   ```

#### 步骤 3.3：重新审查（可选）

修复后如需重新审查：

```
我已经修复了以下问题：
- OrderService 不再直接返回 MyBatis Record
- OrderController 增加了 DTO 转换

请重新审查变更：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：xiangbin/wcctp_optimization
- 目标分支：master
```

---

## 高级用法

### 场景 1：架构审查

当需要审查整体架构质量时：

```
请对我的项目做架构审查：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：feature/arch-refactor
- 目标分支：master
- 审查重点：architecture、module boundary
```

**LLM 会自动：**
- 调用 `java-review-architecture` skill
- 检查 module 之间的依赖方向
- 识别 architecture seam 是否清晰

---

### 场景 2：新增规则提案

当你发现现有规则未覆盖的问题时：

```
我想新增一条审查规则：
- 规则名称：Service 不应直接暴露 cache key 生成逻辑
- 规则类别：semantic-review
- 适用场景：涉及缓存的 service 代码
```

**LLM 会引导你：**
1. 使用 `.openspec/templates/rule-proposal.md` 模板
2. 完成 admission review 流程
3. 添加到规则目录

---

### 场景 3：规则解释

当你对某条规则不理解时：

```
请解释规则 SR-JAVA-PERSISTENCE-001
```

**LLM 会提供：**
- 规则的完整定义
- 适用场景
- 检查清单
- 反模式示例
- 修复建议

---

## 常见问答

### Q1: 为什么有些问题 LLM 不直接指出，而是建议用工具？

**A:** 这是为了降低 LLM 的工作复杂度，同时确保审查的确定性。例如：
- Layer 依赖检查 → ArchUnit 更准确、更快速
- Import 顺序 → Checkstyle 可以自动修复
- 代码复杂度 → PMD 可以给出精确的圈复杂度数值

LLM 应该聚焦在需要业务语义理解的高价值问题上。

---

### Q2: 审查一条 PR 大概需要多久？

**A:** 取决于变更规模：
- 小改动（<5 个文件）：1-2 分钟
- 中等改动（5-20 个文件）：3-5 分钟
- 大改动（>20 个文件）：5-10 分钟

建议按模块拆分 PR，避免一次性审查过多文件。

---

### Q3: 如何确保审查结果的一致性？

**A:** 通过以下机制：
1. **规则化**：每条 finding 必须绑定到具体 rule id
2. **技能聚焦**：不同关注点调用不同的 skill
3. **工具优先**：能用工具检查的就不用 LLM
4. **治理流程**：规则的增删改都经过 admission review

---

### Q4: 可以只审查特定类型的代码吗？

**A:** 可以，通过指定 `审查重点` 参数：

```yaml
审查重点：persistence     # 只审查 repository/DAO 相关
审查重点：exception       # 只审查异常处理相关
审查重点：architecture    # 只审查架构边界
审查重点：sofa           # 只审查 SOFA 相关
```

---

## 最佳实践

### 1. 小步提交，频繁审查

- 每次 PR 控制在 5-10 个文件以内
- 每个功能点单独提 PR
- 避免混合多个不相关的改动

### 2. 分层审查策略

```
第一层：IDE 实时检查（checkstyle/spotless）
  ↓
第二层：本地静态分析（PMD/SpotBugs/ArchUnit）
  ↓
第三层：LLM Semantic Review（本仓库）
```

确保每层只处理它最擅长的问题。

### 3. 明确审查目标

在发起审查前，明确你想要：
- ✅ 发现潜在的 bug 和设计问题 → 使用全量审查
- ✅ 验证特定重构是否正确 → 指定审查重点
- ✅ 学习最佳实践 → 请求详细解释

### 4. 持续沉淀规则

当你发现反复出现的同类问题时：
1. 提案新增规则
2. 完成 admission review
3. 加入规则目录
4. 后续自动检查

---

## 故障排查

### 问题 1：LLM 没有应用任何规则

**可能原因：**
- 规则选择失败
- 规则文件路径错误

**解决方法：**
```bash
# 手动验证规则选择
python3 tools/review/rule_tool.py select \
  --scope review-diff \
  --path <你的文件路径>
```

---

### 问题 2：审查结果过于泛泛

**可能原因：**
- 没有指定审查重点
- 变更文件过多，注意力分散

**解决方法：**
- 指定具体的审查重点（如 `persistence`）
- 拆分 PR，减少单次审查范围

---

### 问题 3：规则引用错误

**可能原因：**
- 规则 id 不存在
- 规则文件语法错误

**解决方法：**
```bash
# 验证规则目录
python3 tools/review/rule_tool.py validate --strict
```

---

## 附录：完整示例

### 完整的审查请求与输出

**用户输入：**
```
请你帮我做代码 CR：
- 仓库路径：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 开发分支：xiangbin/wcctp_optimization
- 目标分支：master
- 审查重点：persistence
```

**LLM 输出：**

```markdown
## Code Review 结果

### 审查范围
- 仓库：/Users/zhehan/Documents/antfin/whale2.0/code/ibcbasis
- 分支：xiangbin/wcctp_optimization → master
- 变更文件：8 个
  - src/main/java/com/example/order/OrderRepository.java
  - src/main/java/com/example/order/OrderService.java
  - src/main/java/com/example/user/UserRepository.java
  - ...
- 应用规则：SR-JAVA-PERSISTENCE-001

---

### Findings

#### 🔴 Major

**问题 1：Repository 方法返回了 MyBatis Record 对象**

- 位置：`OrderRepository.java:34`
- 违反规则：`SR-JAVA-PERSISTENCE-001`
- 问题描述：
  `findAllOrders()` 方法直接返回了 `List<OrderRecord>`，这是 MyBatis 
  生成的 Record 类。这会导致 service layer 代码依赖 MyBatis 的具体实现细节。
  
  当需要更换 ORM 框架或优化查询时，会迫使 service 代码也跟着修改。

- 修复建议：
  ```java
  // ❌ 当前实现
  List<OrderRecord> findAllOrders();
  
  // ✅ 建议实现
  List<Order> findAllOrders();  // Order 是 domain object
  ```

#### 🟡 Minor

**问题 2：Repository 接受了 generic Map 参数**

- 位置：`UserRepository.java:56`
- 违反规则：`SR-JAVA-PERSISTENCE-001`
- 问题描述：
  `findByCondition(Map<String, Object> params)` 方法接受了过于通用的参数，
  这会导致调用方不确定应该传什么 key，也不利于 IDE 的自动补全。

- 修复建议：
  ```java
  // ❌ 当前实现
  List<User> findByCondition(Map<String, Object> params);
  
  // ✅ 建议实现
  List<User> findByCondition(UserQuery query);  // 使用专门的 query object
  ```

---

### Deterministic Routing Suggestions

1. **Layer 依赖检查**
   - 建议工具：ArchUnit
   - 参考规则：`DC-JAVA-SPRING-LAYER-001`
   - 说明：OrderService 直接 import 了 OrderRecord，这应该由 ArchUnit 自动禁止

---

### Rules Consulted

- ✅ SR-JAVA-PERSISTENCE-001 - Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节
```

---

## 总结

通过本手册，你应该已经掌握：

✅ **如何发起审查**：提供仓库路径、分支信息、审查范围  
✅ **审查流程**：用户输入 → LLM 自动选择规则 → 执行审查 → 输出结果  
✅ **如何解读结果**：理解 findings、deterministic suggestions、rules consulted  
✅ **最佳实践**：小步提交、分层审查、持续沉淀规则  

开始使用吧！让你的 Java 代码审查更加高效和一致。
