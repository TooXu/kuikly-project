#!/bin/bash
# Feishu 文件发送脚本
# 用法：./send-feishu-file.sh <文件路径> [消息文本]

FILE_PATH="$1"
MESSAGE="${2:-📄 文件}"

if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 文件不存在：$FILE_PATH"
    exit 1
fi

echo "📤 发送文件到 Feishu..."
echo "   文件：$(basename "$FILE_PATH")"
echo "   消息：$MESSAGE"

# 使用 openclaw message send 发送文件
openclaw message send \
    --channel feishu \
    --target user:ou_f444552b96595ae88251e9988ceb85b7 \
    --media "$FILE_PATH" \
    --message "$MESSAGE" \
    --verbose 2>&1 | tail -20

echo ""
echo "✅ 发送完成"
