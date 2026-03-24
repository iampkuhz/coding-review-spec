# Review 工具说明

`rule_tool.py` 是供 Qoder command 和开发者共同使用的本地工具，用来保证 rule catalog 健康可用。

## 命令

```bash
python3 tools/review/rule_tool.py validate --strict
python3 tools/review/rule_tool.py select --scope review-file --objective persistence --path src/main/java/com/acme/order/OrderService.java
python3 tools/review/rule_tool.py explain --rule SR-JAVA-EXCEPTION-001
```

## 职责

- 校验 schema shape、category 与 admission routing 一致性、跨规则引用关系
- 为当前 review scope 选择最相关的规则
- 在不手工翻 catalog 的情况下解释单条规则

工具会刻意把 deterministic candidate 与 semantic rule 分开，避免 Qoder command 把整本 catalog 都塞进 prompt。
