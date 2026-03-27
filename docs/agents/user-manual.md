# 代码审查用户手册

## 快速开始

### 基本用法

当你需要对 Java 项目进行代码审查时，只需提供以下信息：

```
请你帮我做代码 CR：
- 仓库路径：/path/to/your/repo
- 开发分支：feature-branch
- 目标分支：master
- 审查范围：[可选] 特定文件、模块或全量 diff
- 审查重点：[可选] 例如 persistence、exception、architecture 等
```

### 示例

**示例 1：审查完整的 PR diff**
```
请你帮我做代码 CR：
- 仓库路径：/path/to/repo
- 开发分支：feature/order-optimization
- 目标分支：master
- 审查范围：全量 diff
```

**示例 2：审查特定模块**
```
请你帮我做代码 CR：
- 仓库路径：/path/to/repo
- 开发分支：feature/order-optimization
- 目标分支：master
- 审查范围：order-module 子树
- 审查重点：persistence boundary
```

**示例 3：审查特定文件**
```
请你帮我做代码 CR：
- 仓库路径：/path/to/repo
- 开发分支：feature/order-optimization
- 目标分支：master
- 审查范围：src/main/java/com/example/order/OrderService.java
```

## 完整操作流程

### 阶段 1：用户输入

你需要提供：

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 仓库路径 | ✅ | 目标 git 仓库的本地绝对路径 | `/path/to/repo` |
| 开发分支 | ✅ | 包含变更的特性分支 | `feature/order-optimization` |
| 目标分支 | ✅ | 合并目标分支 | `master` |
| 审查范围 | ❌ | 默认为全量 diff，可指定文件/模块 | `src/main/java/com/example/order/` |
| 审查重点 | ❌ | 指定特定关注点 | `persistence` |

### 阶段 2：AI 自动执行

AI 会自动：

1. 读取规约目录
2. 运行规则选择工具
3. 分析代码变更
4. 生成审查意见

### 阶段 3：用户确认与修复

你需要：

1. 阅读 AI 输出的审查意见
2. 判断每个 finding 是否合理
3. 根据审查意见修复代码

## 高级用法

### 场景 1：架构审查

```
请对我的项目做架构审查：
- 仓库路径：/path/to/repo
- 开发分支：feature/arch-refactor
- 目标分支：master
- 审查重点：architecture、module boundary
```

### 场景 2：新增规约提案

当你发现现有规则未覆盖的问题时：

```
我想新增一条审查规则：
- 规则名称：Service 不应直接暴露 cache key 生成逻辑
- 规则类别：semantic-review
- 适用场景：涉及缓存的 service 代码
```

### 场景 3：规约解释

当你对某条规约不理解时：

```
请解释规则 SR-JAVA-PERSISTENCE-001
```

## 常见问答

### Q: 为什么有些问题 AI 不直接指出，而是建议用工具？

**A:** 这是为了降低 AI 的工作复杂度，同时确保审查的确定性。例如：
- Layer 依赖检查 → ArchUnit 更准确、更快速
- Import 顺序 → Checkstyle 可以自动修复
- 代码复杂度 → PMD 可以给出精确的圈复杂度数值

AI 应该聚焦在需要业务语义理解的高价值问题上。

### Q: 审查一条 PR 大概需要多久？

**A:** 取决于变更规模：
- 小改动（<5 个文件）：1-2 分钟
- 中等改动（5-20 个文件）：3-5 分钟
- 大改动（>20 个文件）：5-10 分钟

建议按模块拆分 PR，避免一次性审查过多文件。

### Q: 如何确保审查结果的一致性？

**A:** 通过以下机制：
1. **规约化**：每条 finding 必须绑定到具体 rule id
2. **技能聚焦**：不同关注点调用不同的 skill
3. **工具优先**：能用工具检查的就不用 AI
4. **治理流程**：规则的增删改都经过 admission review

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
第三层：AI Semantic Review（本手册）
```

确保每层只处理它最擅长的问题。

### 3. 明确审查目标

在发起审查前，明确你想要：
- ✅ 发现潜在的 bug 和设计问题 → 使用全量审查
- ✅ 验证特定重构是否正确 → 指定审查重点
- ✅ 学习最佳实践 → 请求详细解释
