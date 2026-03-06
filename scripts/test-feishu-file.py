#!/usr/bin/env python3
"""
测试 Feishu 文件发送
"""
import base64
from pathlib import Path

# 读取 MD 文件
file_path = Path("/home/admin/.openclaw/workspace/daily-reports/ai-news-daily-2026-03-06.md")
with open(file_path, 'rb') as f:
    file_content = f.read()

# 转换为 Base64
file_base64 = base64.b64encode(file_content).decode('utf-8')

print(f"文件大小：{len(file_content)} bytes")
print(f"Base64 长度：{len(file_base64)} chars")
print(f"\n使用以下参数发送:")
print(f"  buffer: {file_base64[:100]}...")
print(f"  filename: {file_path.name}")
print(f"  mimeType: text/markdown")
