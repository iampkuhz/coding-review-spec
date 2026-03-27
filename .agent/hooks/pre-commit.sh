#!/bin/bash
# Pre-commit 钩子：提交前强制检查

echo "=== Harness Engineering Pre-commit Check ==="

# 运行规则校验
echo "正在校验规则目录..."
python3 .agent/hooks/rule_tool.py validate --strict

if [ $? -ne 0 ]; then
    echo "❌ 规则校验失败"
    exit 1
fi

echo "✅ 所有检查通过"
