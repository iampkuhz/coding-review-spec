# 代码审查规则边界分析

## 目标

本文档明确界定哪些审查规则应该由本地 deterministic 工具（codestyle、spotless、pmd、archunit）处理，哪些应该由 LLM（本仓库）管理，以确保：

1. **工程化管理规约**：避免规约增加导致规约被忽略
2. **降低 LLM 复杂度**：能让工具检查的就不让 LLM 处理
3. **明确的职责边界**：每个工具只处理它最擅长的问题

## 规则分类矩阵

### 1. 应该由本地工具处理的规则（Deterministic）

这类规则的特征：
- **判断标准明确**：可以通过语法分析、静态分析、模式匹配完全确定
- **无业务语义依赖**：不依赖业务逻辑理解
- **稳定性高**：长期不变，适合固化到工具配置

| 检查维度 | 推荐工具 | 典型规则示例 | 仓库中的对应规则 |
|---------|---------|-------------|----------------|
| **代码格式** | checkstyle, spotless | - 命名规范（驼峰、下划线）<br>- 空格、换行、缩进<br>- 括号位置<br>- 行宽限制 | 应归类为 `governance-only` 或移出本仓库 |
| **Import 顺序** | checkstyle, spotless | - import 分组顺序<br>- wildcard import 禁止<br>- 未使用 import | `GV-STYLE-IMPORT-ORDER` 应迁移到 checkstyle |
| **代码复杂度** | pmd, spotbugs | - 圈复杂度超标<br>- 方法过长<br>- 类过大<br>- 嵌套过深 | 应使用 PMD 规则，不在 LLM 管理 |
| **依赖方向** | archunit | - Layer 边界（controller→service→repository）<br>- Module 边界<br>- Package 循环依赖 | `DC-JAVA-SPRING-LAYER-001` 应迁移到 ArchUnit |
| **注解使用** | pmd, custom script | - @Transactional 位置<br>- @RestController vs @Controller<br>- 可见注解缺失 | 部分可迁移到 PMD/ArchUnit |
| **异常声明** | pmd | - 空 catch block<br>- 吞掉异常<br>- 抛出 Exception | 应使用 PMD 规则 |
| **资源关闭** | pmd, spotbugs | - 未关闭 IO 流<br>- 未关闭数据库连接<br>- try-with-resources 缺失 | 应使用 PMD/SpotBugs |
| **空指针风险** | spotbugs | - 可能的 NPE<br>- 未判空访问<br>- Optional 误用 | 应使用 SpotBugs |
| **并发安全** | spotbugs, pmd | - 非线程安全的单例<br>- 竞态条件<br>- 错误的同步 | 应使用 SpotBugs/PMD |
| **SQL 注入风险** | pmd, sonar | - 拼接 SQL<br>- 未使用预编译 | 应使用 PMD/Sonar |
| **日志规范** | checkstyle, pmd | - 日志级别使用<br>- 占位符使用<br>- 吞掉日志 | 应使用 Checkstyle/PMD |

### 2. 应该由 LLM 处理的规则（Semantic Review）

这类规则的特征：
- **需要业务语义理解**：必须理解业务意图才能判断
- **涉及设计质量**：需要评估设计决策的合理性
- **上下文依赖强**：需要跨文件、跨模块理解
- **边界模糊**：无法用简单的规则表达式完整描述

| 检查维度 | 仓库中的对应规则 | 为什么必须 LLM 处理 |
|---------|-----------------|-------------------|
| **Domain Boundary** | `SR-JAVA-DOMAIN-BOUNDARY-001` | 需要理解 aggregate ownership、domain invariant、业务边界，这些无法通过静态分析确定 |
| **Persistence 语义泄漏** | `SR-JAVA-PERSISTENCE-001` | 需要判断 repository API 是否保留了 domain 含义，而不是裸表操作。例如：`save(User user)` vs `activateUser(User user)` 的语义差异 |
| **MVC Controller-Service Handoff** | `SR-JAVA-MVC-CTRL-001` | 需要理解 controller 是否在正确的抽象层级做 transport 处理，service 是否保留了完整的业务语义 |
| **Exception Semantics** | `SR-JAVA-EXCEPTION-001` | 需要理解异常类型选择是否符合业务失败语义，rollback 行为是否正确，error mapping 是否合理 |
| **SOFA Boundary** | `SR-JAVA-SOFA-BOUNDARY-001` | 需要理解 RPC DTO 设计、facade interface 稳定性、跨 module contract、remote error handling |
| **Spring Layering** | `SR-JAVA-SPRING-LAYERING-001` | 需要理解 transaction boundary、orchestration 职责、layer 之间的数据流是否符合业务需求 |
| **Architecture Seam** | `SR-JAVA-ARCHITECTURE-001` | 需要理解 module boundary 设计、dependency direction 是否符合业务架构意图 |

### 3. 灰色地带（需要个案分析）

有些规则初期可能由 LLM 处理，但随着模式稳定，应该迁移到 deterministic 工具：

| 规则类型 | 初期（LLM） | 稳定后（工具） | 迁移条件 |
|---------|-----------|--------------|---------|
| **特定框架使用规范** | LLM 检查 MyBatis XML 写法 | 稳定后写 custom PMD rule | 框架使用模式已统一，团队形成最佳实践 |
| **DTO/Entity 转换** | LLM 检查是否泄漏 | 可写 ArchUnit 规则禁止特定 import | 已经明确哪些 package 不允许互相依赖 |
| **Cache 使用** | LLM 检查 cache key 设计 | 可写 custom script 检查注解使用 | cache 注解使用模式已标准化 |
| **Validation 边界** | LLM 检查 validation 放置位置 | 可写 ArchUnit 规则 | 已明确 validation 只能在哪些 layer |

## 决策流程

当新增一条审查规则时，按以下流程判断归属：

```
1. 这条规则能否用明确的语法/静态分析规则完整描述？
   ├─ 是 → 使用本地工具（checkstyle/pmd/archunit）
   └─ 否 → 继续判断

2. 判断是否需要业务语义理解？
   ├─ 不需要 → 使用本地工具
   └─ 需要 → 继续判断

3. 判断是否需要跨文件/跨模块上下文？
   ├─ 不需要 → 使用本地工具
   └─ 需要 → 继续判断

4. 判断是否涉及设计质量评估（而非对错判断）？
   ├─ 否 → 使用本地工具
   └─ 是 → 放入 LLM semantic review
```

## 工程化建议

### 1. 分层治理架构

```
┌─────────────────────────────────────────┐
│  L1: IDE 实时检查                        │
│  - checkstyle (格式)                     │
│  - spotless (格式化)                     │
│  - 实时反馈，阻断提交                      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  L2: CI 静态分析                         │
│  - PMD (代码质量)                        │
│  - SpotBugs (bug 检测)                    │
│  - ArchUnit (架构约束)                    │
│  - 阻断合并                             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  L3: LLM Semantic Review                │
│  - 本仓库管理                            │
│  - 设计质量评估                          │
│  - 业务语义检查                          │
│  - 辅助决策，不阻断合并                    │
└─────────────────────────────────────────┘
```

### 2. 规则迁移策略

对于当前在 LLM 管理的规则，定期评估是否满足迁移条件：

```yaml
评估周期：每季度一次
评估对象：所有 category=deterministic-candidate 的规则
迁移条件:
  - 模式稳定性：该规则检查的模式已在团队内统一
  - 技术可行性：存在可用的工具（ArchUnit/PMD/Checkstyle）
  - 成本效益：工具实现成本 < LLM 长期消耗成本
```

### 3. 配置管理

**本地工具配置**应该放在：
- `checkstyle.xml` - Checkstyle 规则
- `pmd.xml` - PMD 规则
- `archunit.properties` 或 `*ArchTest.java` - ArchUnit 规则
- `spotbugs-exclude.xml` - SpotBugs 排除规则

**LLM 规则**放在本仓库：
- `.qoder/rules/catalog/semantic/` - 语义审查规则
- `.qoder/rules/catalog/deterministic-candidate/` - 待迁移规则（过渡期）
- `.qoder/rules/catalog/governance-only/` - 治理规则

### 4. 避免规约被忽略的机制

1. **规则数量控制**：
   - Semantic review 规则保持在 5-10 条以内
   - 每条规则必须有明确的 `load_when` 条件
   - 避免全量加载，采用精准命中策略

2. **规则优先级**：
   ```yaml
   severity: critical  # 必须修复
   severity: major     # 应该修复
   severity: minor     # 建议修复
   severity: info      # 仅供参考
   ```

3. **规则有效期**：
   - 每条规则设置 `status`（draft/active/deprecated）
   - 定期 review active 规则的有效性
   - 及时废弃不再适用的规则

4. **工具优先原则**：
   - 在 LLM review 之前，先运行本地工具
   - LLM 只处理本地工具无法覆盖的问题
   - LLM 输出中明确区分："违反工具规则" vs "设计建议"

## 现有规则分类清单

基于当前仓库的规则，分类如下：

### 应保留在 LLM（Semantic Review）
- ✅ `SR-JAVA-PERSISTENCE-001` - Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节
- ✅ `SR-JAVA-DOMAIN-BOUNDARY-001` - DDD domain ownership 检查
- ✅ `SR-JAVA-MVC-CTRL-001` - Controller 到 Service 的 handoff 质量
- ✅ `SR-JAVA-EXCEPTION-001` - Exception semantics 检查
- ✅ `SR-JAVA-SOFA-BOUNDARY-001` - SOFA provider/consumer boundary

### 应迁移到本地工具（Deterministic）
- ⚠️ `DC-JAVA-SPRING-LAYER-001` - Web、application、persistence package 必须保持单向依赖流
  - **目标工具**: ArchUnit
  - **迁移状态**: ready
  - **建议产物**: `src/test/java/.../LayerDependencyArchTest.java`

### 应移除或重新分类
- ❓ `GV-STYLE-IMPORT-ORDER-001` - Import 顺序规则
  - **建议**: 迁移到 Checkstyle，从本仓库移除

## 总结

**核心原则**：
1. **工具优先**：能用 deterministic 工具解决的，绝不用 LLM
2. **语义为王**：LLM 只处理需要业务语义理解的问题
3. **工程化治理**：通过分层架构和明确边界，避免规约膨胀导致失效
4. **持续优化**：定期评估规则归属，推动成熟规则向工具迁移

通过这样的边界划分，可以确保：
- ✅ LLM 的工作负载最小化（只处理高价值问题）
- ✅ 审查结果确定性最大化（工具处理可自动化的问题）
- ✅ 规约管理工程化（清晰的职责和治理流程）
- ✅ 长期可维护性（规则不会无限膨胀）
