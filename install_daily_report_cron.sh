#!/bin/bash
# OpenClaw 日报定时任务安装脚本
# 每天 19:00 自动生成并发送日报

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_SCRIPT="$SCRIPT_DIR/daily_report.py"
PYTHON="${PYTHON:-python3}"

echo "🦞 OpenClaw 日报定时任务安装"
echo "================================"

# 检查 Python
if ! command -v $PYTHON &> /dev/null; then
    echo "❌ 错误：未找到 Python3"
    exit 1
fi

# 检查报告脚本
if [ ! -f "$REPORT_SCRIPT" ]; then
    echo "❌ 错误：未找到报告脚本 $REPORT_SCRIPT"
    exit 1
fi

# 创建 cron 任务
CRON_ENTRY="0 19 * * * cd $SCRIPT_DIR && $PYTHON $REPORT_SCRIPT --send >> /tmp/openclaw-daily-report.log 2>&1"

echo "📋 将添加以下 cron 任务:"
echo "$CRON_ENTRY"
echo ""

# 备份现有 crontab
if command -v crontab &> /dev/null; then
    (crontab -l 2>/dev/null | grep -v "daily_report.py" || true; echo "$CRON_ENTRY") | crontab -
    echo "✅ Cron 任务已安装"
else
    echo "⚠️ 未找到 crontab 命令"
    echo "请手动添加以下任务到 crontab:"
    echo "$CRON_ENTRY"
fi

echo ""
echo "================================"
echo "📊 测试运行报告脚本..."
$PYTHON "$REPORT_SCRIPT"

echo ""
echo "✅ 安装完成！"
echo "下次报告时间：明天 19:00"
