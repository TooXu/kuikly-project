#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime, timezone, timedelta
import re

def parse_session_file(session_file_path, target_date):
    """解析会话文件，提取指定日期的消息"""
    user_messages = []
    assistant_messages = []
    
    try:
        with open(session_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    record = json.loads(line.strip())
                    
                    # 跳过非消息类型
                    if record.get('type') != 'message':
                        continue
                    
                    message_data = record.get('message', {})
                    role = message_data.get('role')
                    timestamp_ms = record.get('timestamp')
                    
                    if not timestamp_ms or not role:
                        continue
                    
                    # 转换时间戳到北京时间
                    beijing_tz = timezone(timedelta(hours=8))
                    msg_time = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).astimezone(beijing_tz)
                    
                    # 检查是否是目标日期
                    if msg_time.date() != target_date:
                        continue
                    
                    # 提取消息内容
                    content_parts = message_data.get('content', [])
                    full_content = ""
                    
                    for part in content_parts:
                        if isinstance(part, dict) and part.get('type') == 'text':
                            text = part.get('text', '')
                            # 移除系统消息前缀
                            if text.startswith("System: ["):
                                continue
                            full_content += text
                    
                    if not full_content.strip():
                        continue
                    
                    formatted_time = msg_time.strftime("%H:%M:%S")
                    
                    if role == 'user':
                        # 清理用户消息中的系统信息
                        cleaned_content = clean_user_message(full_content)
                        if cleaned_content:
                            user_messages.append((formatted_time, cleaned_content))
                    elif role == 'assistant':
                        # 清理助手消息中的工具调用等
                        cleaned_content = clean_assistant_message(full_content)
                        if cleaned_content:
                            assistant_messages.append((formatted_time, cleaned_content))
                            
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    continue
                    
    except FileNotFoundError:
        print(f"会话文件未找到: {session_file_path}")
    except Exception as e:
        print(f"解析会话文件时出错: {e}")
    
    return user_messages, assistant_messages

def clean_user_message(content):
    """清理用户消息，移除系统信息"""
    # 移除系统消息部分
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        if line.strip().startswith("System: [") or "Conversation info" in line:
            continue
        if line.strip().startswith("```json") or line.strip().endswith("```"):
            continue
        if '"conversation_label"' in line:
            continue
        cleaned_lines.append(line)
    
    result = '\n'.join(cleaned_lines).strip()
    return result if result else None

def clean_assistant_message(content):
    """清理助手消息，移除工具调用等技术内容"""
    # 如果包含工具调用，只保留文本部分
    if "toolCall" in content or "toolResult" in content:
        # 尝试提取纯文本回复
        lines = content.split('\n')
        text_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            if '"type":"toolCall"' in line or '"type":"toolResult"' in line:
                continue
            if line.strip().startswith('{"') and line.strip().endswith('}'):
                continue
            text_lines.append(line)
        
        result = '\n'.join(text_lines).strip()
        return result if result else None
    
    return content.strip() if content.strip() else None

def generate_summary(user_messages, assistant_messages, date_str):
    """生成对话总结"""
    summary = f"## 📅 {date_str} 对话总结\n\n"
    
    if user_messages:
        summary += "### 💬 你发送的消息:\n"
        for time, msg in sorted(user_messages, key=lambda x: x[0]):
            summary += f"- **{time}** {msg}\n"
        summary += "\n"
    else:
        summary += "### 💬 你发送的消息:\n今天没有新消息。\n\n"
    
    if assistant_messages:
        summary += "### 🤖 我的回复:\n"
        for time, msg in sorted(assistant_messages, key=lambda x: x[0]):
            summary += f"- **{time}** {msg}\n"
        summary += "\n"
    else:
        summary += "### 🤖 我的回复:\n今天没有回复。\n\n"
    
    return summary

def main():
    print("开始生成每日对话总结...")
    
    # 获取今天的日期（北京时间）
    beijing_tz = timezone(timedelta(hours=8))
    today = datetime.now(beijing_tz).date()
    date_str = today.strftime("%Y-%m-%d")
    
    # 会话文件路径
    session_file = "/home/admin/.openclaw/agents/main/sessions/a724b3c0-8d90-43ba-9974-e1432bf3ad2d.jsonl"
    
    # 解析会话
    user_msgs, assistant_msgs = parse_session_file(session_file, today)
    
    # 生成总结
    summary = generate_summary(user_msgs, assistant_msgs, date_str)
    
    # 保存到文件
    output_file = f"/home/admin/.openclaw/workspace/daily_summary_{date_str}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"每日总结已保存到: {output_file}")
    
    # 打印到控制台以便查看
    print("\n" + "="*50)
    print(summary)
    print("="*50)
    
    print("每日对话总结完成！")

if __name__ == "__main__":
    main()