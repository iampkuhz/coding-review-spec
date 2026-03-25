# 仓库重构总结

## 核心变更

### 1. 规约目录独立

**变更前：**
```
.qoder/rules/  # 混淆在工具配置中
```

**变更后：**
```
rules/  # 独立的项目规约资产
```

**理由：**
- ✅ 规约是项目核心资产，不是工具配置
- ✅ 独立于 Qoder，可以长期维护
- ✅ 清晰可见，新人容易理解
- ✅ 工具中立，可被其他工具复用

---

## 文件移动清单

### 已移动的文件（git mv）

1. `.qoder/rules/README.md` → `rules/README.md`
2. `.qoder/rules/catalog/` → `rules/catalog/`
   - `deterministic-candidate/dc-java-spring-layer-boundary.yaml`
   - `governance-only/gv-style-import-order-reject.yaml`
   - `semantic/sr-java-domain-boundary.yaml`
   - `semantic/sr-java-exception-semantics.yaml`
   - `semantic/sr-java-mvc-controller-service.yaml`
   - `semantic/sr-java-persistence-boundary.yaml`
   - `semantic/sr-java-sofa-boundary.yaml`
3. `.qoder/rules/review-rule-schema.yaml` → `rules/review-rule-schema.yaml`

---

## 已更新的引用

### 1. rule_tool.py

**修改：**
```python
# tools/review/rule_tool.py
-RULE_DIR = ROOT / ".qoder" / "rules" / "catalog"
+RULE_DIR = ROOT / "rules" / "catalog"
```

---

### 2. .openspec/config.yaml

**修改：**
```yaml
-catalog_root: .qoder/rules/catalog
-schema_path: .qoder/rules/review-rule-schema.yaml
+catalog_root: rules/catalog
+schema_path: rules/review-rule-schema.yaml
```

---

### 3. README.md

**修改：**
- 更新"项目概述"章节
- 更新目录结构树
- 明确 `rules/` 是项目核心资产

---

### 4. rules/README.md

**修改：**
```markdown
-这个目录是 Qoder 的项目级 review rule catalog。
+这个目录是项目级的 review rule catalog。
```

---

## 验证结果

```bash
$ python3 tools/review/rule_tool.py validate --strict
已成功校验 7 条 rule 文件。
- deterministic-candidate: 1
- governance-only: 1
- semantic-review: 5
```

✅ 所有规则文件校验通过

---

## 新的目录结构

```
.
├── rules/                          # 审查规约目录（项目核心资产）⭐
│   ├── catalog/                    # 规则分类目录
│   │   ├── deterministic-candidate/
│   │   ├── governance-only/
│   │   └── semantic/
│   └── review-rule-schema.yaml
│
├── .qoder/                         # Qoder 客户端配置
│   ├── commands/
│   └── skills/
│
├── .openspec/                      # OpenSpec 治理配置
│   ├── specs/                      # 模块规约（待添加）
│   ├── workflows/                  # CR 工作流（待添加）
│   └── config.yaml
│
├── docs/                           # 项目文档
│   ├── user-guide.md
│   ├── rule-tool-guide.md
│   ├── rule-concept-explained.md
│   └── review-governance/
│       └── rule-boundary-analysis.md
│
└── tools/
    └── review/
        └── rule_tool.py
```

---

## 后续工作

### 待添加的目录和文件

1. **OpenSpec specs（模块规约）**
   ```
   .openspec/specs/
   ├── module-payment/
   │   ├── spec.md
   │   └── dependencies.md
   ├── module-order/
   │   ├── spec.md
   │   └── dependencies.md
   └── module-user/
       ├── spec.md
       └── dependencies.md
   ```

2. **OpenSpec workflows（CR 工作流）**
   ```
   .openspec/workflows/
   ├── cr-initial-scan.yaml
   ├── cr-deep-dive.yaml
   ├── cr-problem-confirmation.yaml
   └── cr-architecture-gate.yaml
   ```

3. **架构上下文加载器**
   ```
   tools/architecture-context/
   ├── spec-loader.py
   ├── design-doc-loader.py
   └── dependency-graph.py
   ```

---

## 规约维护流程

### 新增规约时

```yaml
步骤：
1. 在 rules/catalog/ 创建规则文件
   # rules/catalog/semantic/sr-java-new-rule.yaml

2. 运行校验
   python3 tools/review/rule_tool.py validate

3. 测试规则
   python3 tools/review/rule_tool.py select \
     --scope review-diff \
     --objective new-rule

4. 提交 PR
```

---

### 更新规约时

```yaml
步骤：
1. 编辑规则文件
   # rules/catalog/semantic/sr-java-existing-rule.yaml

2. 运行校验
   python3 tools/review/rule_tool.py validate

3. 提交 PR
```

---

### 新增模块规约时

```yaml
步骤：
1. 创建模块规约目录
   mkdir .openspec/specs/module-{name}/

2. 创建 spec.md 和 dependencies.md
   # 遵循固定格式

3. 提交 PR
```

---

## 关键设计决策

### 决策 1：rules/ 独立

- **规约是项目资产**，不是工具配置
- **长期维护**，不受工具变更影响
- **工具中立**，可被其他工具复用

### 决策 2：职责分离

```
rules/        → 规约定义（What：审查什么）
.qoder/       → 工具配置（How：如何审查）
.openspec/    → 流程治理（When + Who：何时审查、谁审查）
```

### 决策 3：渐进式丰富

- **第一阶段**：完成 rules/ 独立（✅ 已完成）
- **第二阶段**：添加 OpenSpec specs（待完成）
- **第三阶段**：添加 OpenSpec workflows（待完成）
- **第四阶段**：实现架构上下文加载（待完成）

---

## 总结

✅ **已完成：**
- 规约目录从 `.qoder/rules/` 移动到 `rules/`
- 更新所有引用路径
- 验证规则校验通过
- 更新 README 说明

⏳ **待完成：**
- 添加 OpenSpec specs（模块规约）
- 添加 OpenSpec workflows（CR 工作流）
- 实现架构上下文加载器
- 完善文档

🎯 **核心原则：**
- 规约是项目核心资产
- 工具配置与规约分离
- 长期可维护
- 工具中立
