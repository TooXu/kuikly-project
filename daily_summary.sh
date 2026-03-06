#!/bin/bash
# 每日对话整理脚本
# 在每天19:00执行，整理当天的对话内容并发送给用户

# 获取今天的日期
TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="/home/admin/.openclaw/workspace/memory/${TODAY}.md"

# 检查今天是否有对话记录
if [ -f "$MEMORY_FILE" ]; then
    # 读取今天的对话内容
    CONTENT=$(cat "$MEMORY_FILE")
    
    # 使用OpenClaw发送消息（这里需要根据你的实际配置调整）
    # 由于我们无法直接通过API发送，这里会触发一个本地通知
    echo "【每日对话整理 - $TODAY】"
    echo ""
    echo "$CONTENT"
    
    # 你可以将这个输出通过邮件、Feishu webhook或其他方式发送
    # 具体实现取决于你的服务器配置
    
else
    echo "【每日对话整理 - $TODAY】"
    echo "今天没有对话记录。"
fi