#!/bin/bash

# 每日对话总结脚本
# 在每天19:00执行，总结当天的对话内容

DATE=$(date +"%Y-%m-%d")
LOG_FILE="/home/admin/.openclaw/workspace/memory/${DATE}.md"

# 创建今日记忆文件目录（如果不存在）
mkdir -p /home/admin/.openclaw/workspace/memory

# 获取今天的对话历史（需要通过OpenClaw API）
# 由于我们无法直接访问会话历史，这里使用一个简化方案

# 方案A：如果OpenClaw支持会话历史API
# openclaw sessions history --today > "$LOG_FILE"

# 方案B：创建一个占位符，提醒用户手动触发
SUMMARY_FILE="/home/admin/.openclaw/workspace/daily_summary_${DATE}.txt"

cat > "$SUMMARY_FILE" << EOF
📅 每日对话总结 - $DATE

由于自动化限制，以下是今天的对话总结请求。

请在Feishu中向我发送 "/summary today" 来获取今天的完整对话总结。

或者，您可以配置OpenClaw Gateway配对以启用完全自动化的定时任务。

---
此消息由自动脚本生成
EOF

# 发送提醒到Feishu（需要配置webhook或使用其他方式）
# 这里暂时只生成文件，你可以手动查看

echo "每日总结已生成: $SUMMARY_FILE"