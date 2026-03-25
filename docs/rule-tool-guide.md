# rule_tool.py 使用说明

## 工具概述

`tools/review/rule_tool.py` 是本仓库的核心本地工具，用于：
- 校验规则目录的合法性
- 根据审查场景选择最相关的规则
- 解释单条规则的详细内容

## 命令总览

| 命令 | 用途 | 典型场景 |
|------|------|---------|
| `validate` | 校验规则目录的完整性和一致性 | 新增/修改规则后验证 |
| `select` | 根据审查范围和目标选择规则 | 发起审查前选择规则 |
| `explain` | 查看单条规则的详细信息 | 学习或引用某条规则 |

---

## 命令详解

### 1. validate - 校验规则目录

#### 基本用法

```bash
python3 tools/review/rule_tool.py validate
```

#### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--strict` | flag | ❌ | 要求所有 category 都至少有规则覆盖 |

#### 输出示例

**成功：**
```
已成功校验 7 条 rule 文件。
- deterministic-candidate: 1
- governance-only: 1
- semantic-review: 5
```

**失败：**
```
Rule catalog 校验失败：
- .qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml: 缺少顶层字段：summary
- .qoder/rules/catalog/semantic/sr-java-exception-semantics.yaml: status 必须是 v1
- 检测到重复的 rule id: SR-JAVA-PERSISTENCE-001
```

#### 校验内容

`validate` 命令会检查：

1. **YAML 语法**：文件必须是合法的 YAML 格式
2. **必填字段**：检查所有 required 字段是否存在
   - `schema_version`
   - `id`
   - `title`
   - `summary`
   - `owner`
   - `status`
   - `category`
   - `severity`
   - `profile_tags`
   - `applies_to`
   - `review`
   - `prompt_hints`
   - `governance`

3. **字段值合法性**：
   - `schema_version` 必须是 `v1`
   - `status` 必须是 `draft/active/deprecated/rejected`
   - `category` 必须是 `semantic-review/deterministic-candidate/governance-only`
   - `severity` 必须是 `info/minor/major/critical`

4. **引用完整性**：
   - `governance.related_rules` 引用的 rule id 必须存在
   - `governance.conflicts_with` 引用的 rule id 必须存在

5. **逻辑一致性**：
   - `category=semantic-review` 必须声明 `load_strategy`
   - `category=deterministic-candidate` 必须填写 `deterministic.target_engine`
   - `governance.admission_decision` 必须与 `category` 匹配

#### 使用场景

- ✅ 新增规则后：`python3 tools/review/rule_tool.py validate --strict`
- ✅ 修改规则后：`python3 tools/review/rule_tool.py validate`
- ✅ CI 检查：在 PR 流程中自动运行

---

### 2. select - 选择规则

#### 基本用法

```bash
python3 tools/review/rule_tool.py select --scope <scope> [其他参数]
```

#### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--scope` | string | ✅ | - | 审查范围：<br>`review-diff`, `review-file`, `review-module`, `review-architecture`, `rule-add` |
| `--objective` | string | ❌ | - | 审查重点：<br>`persistence`, `exception`, `architecture`, `sofa` 等 |
| `--path` | string[] | ❌ | - | 变更文件路径列表（可多次指定） |
| `--module` | string | ❌ | - | module 名或 package 名 |
| `--include-governance` | flag | ❌ | false | 是否包含 governance-only 规则 |
| `--limit` | int | ❌ | 8 | 最多返回多少条规则 |

#### 输出示例

**示例 1：根据 scope 选择**
```bash
python3 tools/review/rule_tool.py select \
  --scope review-diff \
  --path src/main/java/com/example/order/OrderService.java
```

输出：
```
# 已选择规则，scope=review-diff
- paths: src/main/java/com/example/order/OrderService.java

## semantic-review
- SR-JAVA-PERSISTENCE-001 | score=6 | Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节
  摘要：Repository API 应保持 service-layer 语义，不应把 persistence entity、mapper DTO、framework-specific query object 或 partial update 语义泄漏到更高层。
  命中原因：path-specific, semantic default

- SR-JAVA-MVC-CTRL-001 | score=5 | Controller 到 Service 的 handoff 质量
  摘要：检查 controller 是否正确处理 transport-layer 关注点，以及 service 是否保留了完整的业务语义。
  命中原因：scope=review-diff, path-keyword

## deterministic-candidate
- DC-JAVA-SPRING-LAYER-001 | score=4 | Web、application、persistence package 必须保持单向依赖流
  摘要：Controller、facade、adapter 代码不应绕过 service 或 application boundary，直接调用 repository、mapper、DAO。
  命中原因：scope=review-diff
  路由：migrate-to-deterministic via archunit
```

**示例 2：指定 objective**
```bash
python3 tools/review/rule_tool.py select \
  --scope review-module \
  --objective persistence \
  --module order-service
```

输出：
```
# 已选择规则，scope=review-module
- objective: persistence
- module: order-service

## semantic-review
- SR-JAVA-PERSISTENCE-001 | score=8 | Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节
  摘要：...
  命中原因：objective=persistence, module=order-service, semantic default
```

#### 评分算法

`select` 命令使用智能评分算法选择最相关的规则：

| 命中条件 | 加分 | 说明 |
|---------|------|------|
| `scope` 匹配 `load_when.scopes` | +3 | 规则明确声明适用于该审查范围 |
| `objective` 匹配 `load_when.objectives` | +3 | 规则明确声明适用于该审查重点 |
| `path` 匹配 `applies_to.paths` | +2 | 文件路径匹配规则声明的适用范围 |
| `module` 匹配 `applies_to.module_patterns` | +2 | module 名匹配规则声明的适用范围 |
| `category=semantic-review` | +1 | 默认给语义审查规则一点权重 |
| `load_by_default=true` | +1 | 规则声明为默认加载 |

**筛选策略：**
1. 只返回 score > 0 的规则
2. 如果有 path/module/objective 等具体目标，只保留针对性命中的规则
3. 只保留最高分的规则（允许 2 分浮动）
4. 最多返回 N 条（默认 8 条）

#### 使用场景

- ✅ Qoder command 自动调用：在 review-diff 等命令中首先执行 select
- ✅ 手动预检查：在发起审查前先看看会应用哪些规则
- ✅ 规则调试：验证某条规则是否能在特定场景下被正确选中

---

### 3. explain - 解释规则

#### 基本用法

```bash
python3 tools/review/rule_tool.py explain --rule <RULE-ID>
```

#### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--rule` | string | ✅ | 规则 ID，如 `SR-JAVA-PERSISTENCE-001` |

#### 输出示例

```bash
python3 tools/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```

输出：
```
# SR-JAVA-PERSISTENCE-001
- 路径：.qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml
- 分类：semantic-review
- 状态：active
- Owner: review-governance@team
- 严重级别：major
- 准入决策：keep-in-semantic-review

Repository API 应保持 service-layer 语义，不应把 persistence entity、mapper DTO、
framework-specific query object 或 partial update 语义泄漏到更高层。

Checklist：
- Repository 暴露的是具备 domain 含义的操作，而不是裸表操作或 mapper 细节。
- Service 代码不依赖 persistence entity、query wrapper 或 mapper 的返回约定。
- Partial update 与 batch write 会把 invariant 显式化，而不是藏进 generic method。

Anti-patterns：
- Service 代码在 persistence boundary 之外直接操作 JPA entity 或 MyBatis record。
- Repository method 从 service 接收 generic map、query wrapper 或 raw SQL fragment。
- Mapper DTO 或 persistence entity 被复用为外部 API payload。

Deterministic routing：
- target engine: archunit
- suggested artifact: src/test/java/.../LayerDependencyArchTest.java
- detection strategy: 用 ArchUnit 明确允许的 package dependency，并禁止 controller 或 facade package import repository、mapper、DAO package。
```

#### 使用场景

- ✅ 学习规则：理解某条规则的完整定义
- ✅ 审查引用：在审查结果中引用规则详情
- ✅ 规则治理：查看规则的治理决策和迁移建议

---

## 规则在哪里维护/查看

### 规则存储位置

所有规则都存储在 `.qoder/rules/catalog/` 目录下：

```
.qoder/rules/catalog/
├── semantic/                  # 语义审查规则（LLM 处理）
│   ├── sr-java-persistence-boundary.yaml
│   ├── sr-java-domain-boundary.yaml
│   ├── sr-java-exception-semantics.yaml
│   ├── sr-java-mvc-controller-service.yaml
│   └── sr-java-sofa-boundary.yaml
├── deterministic-candidate/   # 待迁移工具规则
│   └── dc-java-spring-layer-boundary.yaml
└── governance-only/           # 治理规则
    └── gv-style-import-order-reject.yaml
```

### 规则查看方式

#### 方式 1：直接查看 YAML 文件

```bash
cat .qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml
```

#### 方式 2：使用 explain 命令

```bash
python3 tools/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
```

#### 方式 3：在线浏览（如果部署了 Web UI）

```
http://<your-domain>/rules/SR-JAVA-PERSISTENCE-001
```

---

## 当前支持的规则列表

### Semantic Review 规则（LLM 处理）

| Rule ID | 标题 | 适用场景 | 严重级别 |
|---------|------|---------|---------|
| `SR-JAVA-PERSISTENCE-001` | Repository 与 persistence boundary 不应向上泄漏 ORM 或 mapper 细节 | 涉及 repository、mapper、DAO、persistence contract 的代码 | major |
| `SR-JAVA-DOMAIN-BOUNDARY-001` | DDD domain ownership 检查 | 涉及 aggregate、domain service、domain invariant 的代码 | major |
| `SR-JAVA-MVC-CTRL-001` | Controller 到 Service 的 handoff 质量 | 涉及 controller、facade、request mapping 的代码 | major |
| `SR-JAVA-EXCEPTION-001` | Exception semantics 检查 | 涉及 exception type、catch block、rollback、error mapping 的代码 | major |
| `SR-JAVA-SOFA-BOUNDARY-001` | SOFA provider/consumer boundary | 涉及 SOFA facade、provider adapter、consumer、RPC DTO 的代码 | major |
| `SR-JAVA-SPRING-LAYERING-001` | Spring layering 与职责放置 | 涉及 controller、service、application service、transaction 的代码 | major |
| `SR-JAVA-ARCHITECTURE-001` | Architecture seam 与 module boundary | 涉及 module boundary、dependency direction 的代码 | major |

### Deterministic Candidate 规则（应迁移到工具）

| Rule ID | 标题 | 目标工具 | 迁移状态 |
|---------|------|---------|---------|
| `DC-JAVA-SPRING-LAYER-001` | Web、application、persistence package 必须保持单向依赖流 | ArchUnit | ready |

### Governance Only 规则（仅治理使用）

| Rule ID | 标题 | 用途 |
|---------|------|------|
| `GV-STYLE-IMPORT-001` | Import 顺序规则 | 应迁移到 Checkstyle |

---

## 规则元数据说明

每条规则都包含以下关键元数据：

### 基础信息

```yaml
schema_version: v1           # 规则 schema 版本
id: SR-JAVA-PERSISTENCE-001  # 唯一标识符
title: ...                   # 规则标题
summary: ...                 # 一句话摘要
owner: ...                   # 规则负责人
status: active               # 状态：draft/active/deprecated/rejected
category: semantic-review    # 分类
severity: major              # 严重级别
```

### 适用范围

```yaml
applies_to:
  languages: [java]          # 适用语言
  frameworks: [spring]       # 适用框架
  module_patterns:           # module 命名模式
    - "*-service"
    - "*-repository"
  paths:                     # 文件路径模式
    - "**/*Repository.java"
    - "**/*Dao.java"
  package_patterns:          # package 模式
    - "..repository.."
    - "..service.."
```

### 审查定义

```yaml
review:
  objective: ...             # 审查目标
  checklist: [...]           # 检查清单
  positive_indicators: [...] # 正面指标
  anti_patterns: [...]       # 反模式
  comment_contract: ...      # 评论约定
```

### Prompt 提示

```yaml
prompt_hints:
  load_by_default: true      # 是否默认加载
  load_when:                 # 何时加载
    scopes: [review-diff, review-file]
    objectives: [persistence]
  max_context_lines: 120     # 最大上下文行数
  prefer_when_profiles: [...] # 优先使用场景
```

### 治理信息

```yaml
governance:
  admission_decision: keep-in-semantic-review  # 准入决策
  rationale: ...               # 决策理由
  evidence_required: [...]     # 需要的证据
  conflicts_with: [...]        # 冲突的规则
  supersedes: [...]            # 替代的规则
  related_rules: [...]         # 相关的规则
```

### Deterministic 信息（仅 deterministic-candidate）

```yaml
deterministic:
  target_engine: archunit    # 目标工具
  migration_readiness: ready # 迁移就绪状态
  suggested_artifact: ...    # 建议的产物
  detection_strategy: ...    # 检测策略
```

---

## 最佳实践

### 1. 在 CI 中集成 validate

```yaml
# .github/workflows/validate-rules.yml
name: Validate Rule Catalog
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate rules
        run: python3 tools/review/rule_tool.py validate --strict
```

### 2. 在审查前自动 select

```python
# 在 Qoder command 中
def run_review(scope, paths, objective=None):
    # 先选择规则
    result = subprocess.run([
        'python3', 'tools/review/rule_tool.py', 'select',
        '--scope', scope,
        '--path', *paths,
        '--objective', objective or ''
    ], capture_output=True, text=True)
    
    # 解析选中的规则
    selected_rules = parse_select_output(result.stdout)
    
    # 只加载 semantic-review 规则
    semantic_rules = [r for r in selected_rules if r['category'] == 'semantic-review']
    
    # 执行审查
    return execute_review(semantic_rules, paths)
```

### 3. 在审查结果中引用规则

```markdown
## Findings

### 问题 1：Repository 泄漏 persistence 细节

- 违反规则：`SR-JAVA-PERSISTENCE-001`
- 规则摘要：Repository API 应保持 service-layer 语义...
- 查看规则详情：
  ```bash
  python3 tools/review/rule_tool.py explain --rule SR-JAVA-PERSISTENCE-001
  ```
```

### 4. 定期审查规则有效性

```bash
# 每季度执行一次全面审查
python3 tools/review/rule_tool.py validate --strict
python3 tools/review/rule_tool.py select --scope review-architecture --limit 20
```

---

## 故障排查

### 问题 1：validate 失败

**错误信息：**
```
Rule catalog 校验失败：
- .qoder/rules/catalog/semantic/sr-java-persistence-boundary.yaml: 缺少顶层字段：summary
```

**解决方法：**
1. 打开报错的文件
2. 检查是否缺少必填字段
3. 参考 `review-rule-schema.yaml` 补充字段

---

### 问题 2：select 返回空结果

**错误信息：**
```
没有匹配到目标规则。可以尝试更宽的 objective，或启用 governance 规则。
```

**解决方法：**
1. 检查 `--scope` 参数是否正确
2. 检查 `--path` 是否在规则的 `applies_to.paths` 范围内
3. 尝试移除 `--objective` 参数扩大范围
4. 添加 `--include-governance` 包含治理规则

---

### 问题 3：explain 找不到规则

**错误信息：**
```
未找到规则：SR-JAVA-PERSISTENCE-001
```

**解决方法：**
1. 检查 rule id 是否拼写正确
2. 运行 `python3 tools/review/rule_tool.py validate` 检查规则文件是否正常
3. 确认规则文件在正确的 category 目录下

---

## 总结

`rule_tool.py` 是本仓库的核心工具，提供了：

✅ **validate** - 确保规则目录的完整性和一致性  
✅ **select** - 智能选择最相关的规则  
✅ **explain** - 查看规则完整定义  

规则存储在 `.qoder/rules/catalog/` 目录下，按 category 分类管理。

通过本工具，可以确保：
- 规则管理工程化
- 规则选择智能化
- 规则学习便捷化
