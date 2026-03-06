#!/usr/bin/env python3
"""
记忆蒸馏工具
功能：
1. 扫描指定日期范围的日志
2. 提取关键信息（决策、教训、偏好、技能）
3. 生成 MEMORY.md 更新建议
4. 归档旧日志
"""
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/admin/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
ARCHIVE_DIR = MEMORY_DIR / "archive"
MEMORY_FILE = WORKSPACE / "MEMORY.md"

# 提取模式
PATTERNS = {
    "决策": [r"决定 [到定].*?[:：]\s*(.+)", r"已确认 [：:]\s*(.+)", r"采用 [了到].*?[:：]\s*(.+)"],
    "教训": [r"经验教训 [\s\S]*?(?=\n##|\Z)", r"教训 [：:]\s*(.+)", r"错误 [：:]\s*(.+)"],
    "偏好": [r"偏好 [：:]\s*(.+)", r"喜欢 [使用].*?[:：]\s*(.+)", r"推荐 [使用].*?[:：]\s*(.+)"],
    "技能": [r"已安装 [技能].*?[:：]\s*(.+)", r"新技能 [：:]\s*(.+)", r"学会 [了到].*?[:：]\s*(.+)"],
    "配置": [r"配置 [更新修改].*?[:：]\s*(.+)", r"规则 [更新].*?[:：]\s*(.+)"],
}

def extract_insights(content, date_str):
    """从日志内容中提取关键信息"""
    insights = []
    
    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[-1]  # 取最后一个分组
                insights.append({
                    "date": date_str,
                    "category": category,
                    "content": match.strip()
                })
    
    return insights

def read_log_file(filepath):
    """读取日志文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取失败 {filepath}: {e}")
        return ""

def get_logs_in_range(days=7):
    """获取指定天数内的日志文件"""
    logs = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        log_file = MEMORY_DIR / f"{date_str}.md"
        
        if log_file.exists():
            logs.append({
                "file": log_file,
                "date": date_str,
                "content": read_log_file(log_file)
            })
    
    return logs

def generate_distillation_report(logs):
    """生成蒸馏报告"""
    all_insights = []
    
    for log in logs:
        insights = extract_insights(log["content"], log["date"])
        all_insights.extend(insights)
    
    # 按类别分组
    by_category = {}
    for insight in all_insights:
        cat = insight["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(insight)
    
    return by_category

def format_for_memory(by_category):
    """格式化为 MEMORY.md 更新内容"""
    output = []
    output.append(f"## 🕐 自动蒸馏更新 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    
    for category, insights in by_category.items():
        if insights:
            output.append(f"### {category}")
            for insight in insights[:5]:  # 每个类别最多 5 条
                output.append(f"- [{insight['date']}] {insight['content']}")
            output.append("")
    
    return "\n".join(output)

def archive_old_logs(days_old=7):
    """归档旧日志"""
    archived = []
    today = datetime.now()
    
    ARCHIVE_DIR.mkdir(exist_ok=True)
    
    for file in MEMORY_DIR.glob("*.md"):
        # 跳过非日期格式的文件
        match = re.match(r"(\d{4}-\d{2}-\d{2})\.md", file.name)
        if not match:
            continue
        
        file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
        age_days = (today - file_date).days
        
        if age_days > days_old:
            dest = ARCHIVE_DIR / file.name
            file.rename(dest)
            archived.append(file.name)
    
    return archived

def main():
    print("🔮 开始记忆蒸馏流程...\n")
    
    # 1. 读取最近 7 天日志
    print("📖 读取最近 7 天日志...")
    logs = get_logs_in_range(7)
    print(f"   找到 {len(logs)} 个日志文件\n")
    
    # 2. 提取关键信息
    print("⚗️  提取关键信息...")
    report = generate_distillation_report(logs)
    
    # 3. 生成更新建议
    print("📝 生成 MEMORY.md 更新建议...\n")
    print("=" * 60)
    update_suggestion = format_for_memory(report)
    print(update_suggestion)
    print("=" * 60 + "\n")
    
    # 4. 归档旧日志
    print("📦 归档 7 天前的日志...")
    archived = archive_old_logs(7)
    if archived:
        print(f"   已归档 {len(archived)} 个文件:")
        for f in archived:
            print(f"   - {f}")
    else:
        print("   无需归档")
    
    print("\n✅ 蒸馏完成！")
    print("\n💡 下一步：")
    print("   1. 审查上面的更新建议")
    print("   2. 手动将重要内容添加到 MEMORY.md")
    print("   3. 或运行 AI 辅助更新：openclaw run '更新 MEMORY.md'")

if __name__ == "__main__":
    main()
