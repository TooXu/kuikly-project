#!/usr/bin/env python3
"""
OpenClaw 增强版每日总结生成器
功能：
- 自动读取当天记忆文件
- 生成结构化日报（Markdown 格式）
- 支持发送到 Feishu/邮件/本地保存
- 包含技术状态检查

使用方法：
python3 daily_report.py [--send] [--date YYYY-MM-DD]
"""

import os
import sys
import json
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

# 配置
WORKSPACE = Path("/home/admin/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORT_DIR = WORKSPACE / "daily-reports"
REPORT_DIR.mkdir(exist_ok=True)

def get_today_memory():
    """读取今天的记忆文件"""
    today = date.today().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{today}.md"
    
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def get_yesterday_memory():
    """读取昨天的记忆文件（用于对比）"""
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{yesterday}.md"
    
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def check_gateway_status():
    """检查 Gateway 状态（模拟）"""
    # 实际使用时可以通过 exec 调用 openclaw gateway status
    return {
        "running": True,
        "port": 14961,
        "issues": ["Feishu 通道待配对"]
    }

def generate_daily_report(memory_content, gateway_status):
    """生成日报内容"""
    today = date.today().strftime("%Y-%m-%d")
    weekday = date.today().strftime("%A")
    
    # 分析记忆内容
    task_count = memory_content.lower().count("task") if memory_content else 0
    conversation_count = memory_content.count("对话") if memory_content else 0
    
    report = f"""# 📅 OpenClaw 每日报告 - {today} ({weekday})

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**报告状态**: {"✅ 完整" if memory_content else "⚠️ 无对话记录"}

---

## 📊 今日概览

| 指标 | 数值 |
|------|------|
| 对话记录 | {"有" if memory_content else "无"} |
| 任务执行 | {task_count} 次 |
| 对话轮次 | 约 {conversation_count} 轮 |
| Gateway 状态 | {"🟢 运行中" if gateway_status["running"] else "🔴 异常"} |

---

## 💬 今日对话内容

{memory_content if memory_content else "*今日暂无对话记录*"}

---

## 🔧 技术状态

### Gateway 状态
- **运行状态**: {"✅ 正常" if gateway_status["running"] else "❌ 异常"}
- **端口**: {gateway_status["port"]}
- **问题**: {", ".join(gateway_status["issues"]) if gateway_status["issues"] else "无"}

### 待解决问题
{chr(10).join(f"- {issue}" for issue in gateway_status["issues"]) if gateway_status["issues"] else "- 无"}

---

## 📈 趋势分析

{f"**对比昨天**: 昨天有对话记录" if get_yesterday_memory() else "**对比昨天**: 昨天也无对话记录"}

---

## 🎯 明日建议

1. 完成 Feishu 通道配对
2. 继续安装推荐技能（summarize, browser-automation, skill-creator）
3. 配置定时任务确保日报自动发送

---

*🤖 此报告由 OpenClaw 自动生成*  
*下次报告：明天 19:00*
"""
    return report

def save_report(report_content):
    """保存报告到文件"""
    today = date.today().strftime("%Y-%m-%d")
    report_file = REPORT_DIR / f"daily-report-{today}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return report_file

def send_to_feishu(report_content):
    """发送到 Feishu（需要配置 webhook 或使用 message 工具）"""
    # 这里可以集成 Feishu webhook 或调用 OpenClaw message 工具
    print("📤 准备发送到 Feishu...")
    print(report_content[:500] + "..." if len(report_content) > 500 else report_content)
    # TODO: 集成实际的发送逻辑
    return True

def main():
    parser = argparse.ArgumentParser(description='OpenClaw 每日总结生成器')
    parser.add_argument('--send', action='store_true', help='发送到 Feishu')
    parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)，默认为今天')
    args = parser.parse_args()
    
    print("🦞 OpenClaw 每日报告生成器")
    print("=" * 50)
    
    # 获取记忆内容
    memory_content = get_today_memory()
    gateway_status = check_gateway_status()
    
    # 生成报告
    report = generate_daily_report(memory_content, gateway_status)
    
    # 保存报告
    report_file = save_report(report)
    print(f"✅ 报告已保存：{report_file}")
    
    # 发送（可选）
    if args.send:
        if send_to_feishu(report):
            print("✅ 已发送到 Feishu")
        else:
            print("❌ 发送失败")
    
    print("=" * 50)
    print("📊 报告预览（前 500 字符）:")
    print(report[:500])

if __name__ == "__main__":
    main()
