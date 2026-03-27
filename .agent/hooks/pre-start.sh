#!/bin/bash
# Pre-start 钩子：Agent 启动前校验

echo "=== Harness Engineering Pre-start Check ==="

# 检查必要文件是否存在
if [ ! -f ".agent/tool-profiles.json" ]; then
    echo "❌ 错误：缺少 .agent/tool-profiles.json"
    exit 1
fi

if [ ! -d ".agent/rules-catalog" ]; then
    echo "❌ 错误：缺少 .agent/rules-catalog"
    exit 1
fi

echo "✅ 所有必要文件存在"
