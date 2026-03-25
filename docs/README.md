# 文档索引

这是本仓库的文档导航页面，帮助你快速找到所需信息。

---

## 📚 按角色分类

### 作为代码审查用户

你想使用本仓库进行 Java 代码审查：

| 文档 | 用途 | 阅读时间 |
|------|------|---------|
| [**用户操作手册**](user-guide.md) | 学习如何发起审查、操作流程、完整示例 | 15 分钟 |
| [**如何运行 Review**](review-governance/how-to-run-review.md) | 快速查看 Qoder commands 用法 | 5 分钟 |

**推荐阅读顺序：** 用户操作手册 → 如何运行 Review

---

### 作为规则治理者

你想管理审查规则，确保规约工程化：

| 文档 | 用途 | 阅读时间 |
|------|------|---------|
| [**规则边界分析**](review-governance/rule-boundary-analysis.md) | 理解哪些规则应该由工具处理，哪些由 LLM 处理 | 20 分钟 |
| [**如何添加规则**](review-governance/how-to-add-a-rule.md) | 学习规则的提案、准入、修改、废弃流程 | 10 分钟 |

**推荐阅读顺序：** 规则边界分析 → 如何添加规则

---

### 作为仓库维护者

你想深入理解仓库设计和实现：

| 文档 | 用途 | 阅读时间 |
|------|------|---------|
| [**rule_tool.py 使用指南**](rule-tool-guide.md) | 本地规则校验与选择工具详解 | 20 分钟 |
| [**Rule 概念解析**](rule-concept-explained.md) | 深入理解 Rule 的本质和组织方式 | 15 分钟 |

**推荐阅读顺序：** Rule 概念解析 → rule_tool.py 使用指南

---

## 📖 按主题分类

### 主题 1：如何使用代码审查

**场景：** 你有一个 Java 项目需要审查

```
1. 阅读 [用户操作手册](user-guide.md)
   └─ 学习基本用法、完整流程、示例
   
2. 参考 [如何运行 Review](review-governance/how-to-run-review.md)
   └─ 查看具体的 command 用法
   
3. 如需深入理解规则选择逻辑
   └─ 阅读 [rule_tool.py 使用指南](rule-tool-guide.md) 的 select 命令章节
```

---

### 主题 2：如何工程化管理规约

**场景：** 你想确保规约不会无限膨胀，保持可维护性

```
1. 阅读 [规则边界分析](review-governance/rule-boundary-analysis.md)
   └─ 理解工具优先原则、分层治理架构
   
2. 学习 [如何添加规则](review-governance/how-to-add-a-rule.md)
   └─ 掌握规则的准入流程和治理机制
   
3. 深入理解 [Rule 概念解析](rule-concept-explained.md)
   └─ 理解 Rule 的双重身份：规约 + 上下文
```

---

### 主题 3：如何理解 Rule 的本质

**场景：** 你对 Rule 的组织方式有疑问

```
1. 必读 [Rule 概念解析](rule-concept-explained.md)
   └─ 解答：Rule 是上下文还是规约？
   
2. 参考 [rule_tool.py 使用指南](rule-tool-guide.md)
   └─ 查看 Rule 的存储结构、元数据、生命周期
   
3. 延伸阅读 [规则边界分析](review-governance/rule-boundary-analysis.md)
   └─ 理解为什么有些 Rule 应该由工具处理
```

---

### 主题 4：如何优化规则体系

**场景：** 你想优化现有的规则体系，推动规则向工具迁移

```
1. 阅读 [规则边界分析](review-governance/rule-boundary-analysis.md)
   └─ 学习决策流程、迁移策略、工程化建议
   
2. 参考 [rule_tool.py 使用指南](rule-tool-guide.md)
   └─ 了解规则的 category 分类和治理信息
   
3. 学习 [如何添加规则](review-governance/how-to-add-a-rule.md)
   └─ 掌握规则的完整生命周期管理
```

---

## 🎯 快速查找

### 我想...

| 需求 | 推荐文档 | 章节 |
|------|---------|------|
| 快速发起一次审查 | [用户操作手册](user-guide.md) | 快速开始 |
| 理解审查流程 | [用户操作手册](user-guide.md) | 完整操作流程 |
| 知道要提供什么信息 | [用户操作手册](user-guide.md) | 阶段 1：用户输入 |
| 了解 LLM 会自动做什么 | [用户操作手册](user-guide.md) | 阶段 2：Spec 自动执行 |
| 理解哪些规则由工具处理 | [规则边界分析](review-governance/rule-boundary-analysis.md) | 规则分类矩阵 |
| 学习 rule_tool.py 的用法 | [rule_tool.py 使用指南](rule-tool-guide.md) | 命令详解 |
| 理解 Rule 是什么 | [Rule 概念解析](rule-concept-explained.md) | Rule 的双重身份 |
| 新增一条规则 | [如何添加规则](review-governance/how-to-add-a-rule.md) | 完整流程 |
| 验证规则目录 | [rule_tool.py 使用指南](rule-tool-guide.md) | validate 命令 |
| 查看某条规则详情 | [rule_tool.py 使用指南](rule-tool-guide.md) | explain 命令 |

---

## 📋 文档清单

### 核心文档（必读）

- ✅ [README](../README.md) - 项目概述
- ✅ [用户操作手册](user-guide.md) - 如何使用审查助手
- ✅ [规则边界分析](review-governance/rule-boundary-analysis.md) - 工具 vs LLM 职责划分

### 使用指南（推荐）

- ✅ [如何运行 Review](review-governance/how-to-run-review.md) - Qoder commands 快速参考
- ✅ [rule_tool.py 使用指南](rule-tool-guide.md) - 本地工具详解

### 深入理解（进阶）

- ✅ [Rule 概念解析](rule-concept-explained.md) - Rule 的本质和组织方式
- ✅ [如何添加规则](review-governance/how-to-add-a-rule.md) - 规则治理流程

---

## 🔗 相关资源

### 仓库结构

```
docs/
├── README.md (本文件)
├── user-guide.md                          # 用户操作手册
├── rule-tool-guide.md                     # rule_tool.py 使用指南
├── rule-concept-explained.md              # Rule 概念解析
└── review-governance/
    ├── README.md
    ├── how-to-run-review.md               # 如何运行 Review
    ├── how-to-add-a-rule.md               # 如何添加规则
    └── rule-boundary-analysis.md          # 规则边界分析
```

### 规则目录

```
.qoder/rules/catalog/
├── semantic/                  # 语义审查规则（LLM 处理）
├── deterministic-candidate/   # 待迁移工具规则
└── governance-only/           # 治理规则
```

### 工具脚本

```
tools/review/
└── rule_tool.py               # 核心本地工具
```

---

## 💡 建议的阅读路径

### 路径 1：快速上手（30 分钟）

```
1. README (5 分钟)
   └─ 了解项目概述
   
2. 用户操作手册 - 快速开始 (10 分钟)
   └─ 学习基本用法
   
3. 如何运行 Review (5 分钟)
   └─ 查看 command 用法
   
4. 实际发起一次审查 (10 分钟)
   └─ 实践出真知
```

---

### 路径 2：系统学习（2 小时）

```
1. README (5 分钟)
   
2. 用户操作手册 - 完整流程 (20 分钟)
   └─ 理解全过程
   
3. 规则边界分析 (30 分钟)
   └─ 理解设计哲学
   
4. rule_tool.py 使用指南 (30 分钟)
   └─ 掌握工具用法
   
5. Rule 概念解析 (20 分钟)
   └─ 深入理解本质
   
6. 如何添加规则 (15 分钟)
   └─ 学习治理流程
```

---

### 路径 3：深度学习（4 小时）

```
1. 通读所有文档 (2 小时)
   
2. 实践：发起多次审查 (1 小时)
   
3. 实践：新增或修改一条规则 (30 分钟)
   
4. 实践：运行 validate 和 select (30 分钟)
```

---

## 📞 问题排查

如果你在阅读或使用过程中遇到问题：

1. **先查文档索引**（本页面）
2. **再查对应文档的故障排查章节**
   - [用户操作手册 - 故障排查](user-guide.md#故障排查)
   - [rule_tool.py 使用指南 - 故障排查](rule-tool-guide.md#故障排查)
3. **查看示例**
   - [用户操作手册 - 完整示例](user-guide.md#附录完整示例)
4. **如果仍有疑问**，可以：
   - 发起 GitHub Issue
   - 联系仓库维护者

---

## 📝 文档维护

### 文档更新记录

- 2026-03-25：创建文档索引和四篇核心文档
  - 用户操作手册
  - 规则边界分析
  - rule_tool.py 使用指南
  - Rule 概念解析

### 贡献指南

如果你想改进文档：

1. 确保文档结构清晰
2. 提供具体示例
3. 保持术语一致
4. 遵循现有文档风格

---

## 总结

通过本文档索引，你应该能够：

✅ **快速找到**所需的文档  
✅ **理解文档之间的关系**  
✅ **选择合适的学习路径**  
✅ **高效掌握仓库使用方法**

开始你的代码审查之旅吧！
