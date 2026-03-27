#!/bin/bash
# Post-failure 钩子：失败时自动收集诊断信息

echo "=== Harness Engineering Failure Diagnosis ==="

# 收集诊断信息
echo "收集诊断信息..."
echo "时间：$(date)"
echo "当前目录：$(pwd)"
echo "最近提交：$(git log -1 --oneline)"

# 如果有规则校验失败，输出详细信息
if [ -n "$1" ]; then
    echo "失败原因：$1"
fi
