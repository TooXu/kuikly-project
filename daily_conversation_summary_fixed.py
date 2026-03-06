#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日对话总结脚本 - 修复版本
在每天19:00执行，总结当天的对话内容并通过Feishu发送
"""

import json
import os
from datetime import datetime, timezone, timedelta
import requests

def get_beijing_time():
    """获取北京时间"""
    beijing_tz = timezone(timedelta(hours=8))
    return datetime.now(beijing_tz)

def parse_session_file(session_file_path):
    """解析会话文件，提取今天的对话"""
    messages = []
    today = get_beijing_time().strftime("%Y-%m-%d")
    
    if not os.path.exists(session_file_path):
        return messages
        
    with open(session_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line.strip())
                if record.get('type') == 'message' and 'message' in record:
                    msg_data = record['message']
                    # 转换时间戳为北京时间
                    timestamp_ms = record.get('timestamp', 0)
                    if isinstance(timestamp_ms, str):
                        continue
                    msg_time = datetime.fromtimestamp(timestamp_ms / 1000, timezone(timedelta(hours=8)))
                    msg_date = msg_time.strftime("%Y-%m-%d")
                    
                    if msg_date == today:
                        role = msg_data.get('role', '')
                        content_parts = msg_data.get('content', [])
                        content_text = ""
                        for part in content_parts:
                            if isinstance(part, dict) and part.get('type') == 'text':
                                content_text = part.get('text', '')
                                break
                            elif isinstance(part, str):
                                content_text = part
                                break
                        
                        if content_text:
                            time_str = msg_time.strftime("%H:%M:%S")
                            messages.append({
                                'time': time_str,
                                'role': role,
                                'content': content_text
                            })
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                continue
    
    return messages

def generate_summary(messages):
    """生成对话总结"""
    today = get_beijing_time().strftime("%Y-%m-%d")
    user_messages = []
    assistant_messages = []
    
    for msg in messages:
        if msg['role'] == 'user':
            user_messages.append(f"**{msg['time']}** - {msg['content']}")
        elif msg['role'] == 'assistant':
            # 过滤掉系统消息和工具调用
            if not msg['content'].startswith(('✅ New session', 'Command still running', 'Process')):
                assistant_messages.append(f"**{msg['time']}** - {msg['content']}")
    
    summary = f"""## 📅 {today} 对话总结

### 💬 你发送的消息:
{chr(10).join(user_messages) if user_messages else "今天没有新消息。"}

### 🤖 我的回复:
{chr(10).join(assistant_messages) if assistant_messages else "今天没有回复。"}

---
✅ 自动化总结任务已启用
"""
    return summary

def send_to_feishu(summary):
    """通过Feishu发送总结（这里先保存到文件）"""
    today = get_beijing_time().strftime("%Y-%m-%d")
    summary_file = f"/home/admin/.openclaw/workspace/daily_summary_{today}.md"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"每日总结已生成: {summary_file}")
    return summary_file

def main():
    print("开始生成每日对话总结...")
    
    # 会话文件路径
    session_file = "/home/admin/.openclaw/agents/main/sessions/a724b3c0-8d90-43ba-9974-e1432bf3ad2d.jsonl"
    
    # 解析会话
    messages = parse_session_file(session_file)
    
    # 生成总结
    summary = generate_summary(messages)
    
    # 保存并发送
    summary_file = send_to_feishu(summary)
    
    print("每日对话总结完成！")
    print("\n" + "="*50)
    print(summary)
    print("="*50)

if __name__ == "__main__":
    main()