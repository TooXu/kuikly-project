#!/usr/bin/env python3
"""
🧠 自动学习记录器 - 傅盛三万风格
核心理念：犯错 → 写规则 → 变 Skill → Never Again

功能：
- 自动检测对话中的学习事件
- 生成标准化的学习条目
- 支持优先级分类和标签
- 定期回顾和促进到系统规则

使用方法：
python3 auto-learn.py --type learning --message "用户纠正了配置修改方式"
python3 auto-learn.py --type error --command "openclaw restart" --error "Invalid config"
python3 auto-learn.py --review  # 回顾待促进的学习
"""

import os
import sys
import json
import argparse
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, List

# ==================== 配置区域 ====================
WORKSPACE = Path("/home/admin/.openclaw/workspace")
LEARNINGS_DIR = WORKSPACE / ".learnings"
MEMORY_DIR = WORKSPACE / "memory"

# 确保目录存在
LEARNINGS_DIR.mkdir(exist_ok=True)

# 学习类型
LEARNING_TYPES = {
    "learning": "LEARNINGS.md",
    "error": "ERRORS.md",
    "feature": "FEATURE_REQUESTS.md"
}

# 优先级映射
PRIORITY_MAP = {
    "critical": "🔴 严重",
    "high": "🟠 高",
    "medium": "🟡 中",
    "low": "🟢 低"
}

# ==================== 辅助函数 ====================

def generate_id(entry_type: str) -> str:
    """生成学习条目 ID"""
    today = date.today().strftime("%Y%m%d")
    prefix = {
        "learning": "LRN",
        "error": "ERR",
        "feature": "FEAT"
    }[entry_type]
    
    # 计算今日序号
    file_path = LEARNINGS_DIR / LEARNING_TYPES[entry_type]
    count = 1
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            today_prefix = f"{prefix}-{today}-"
            count = content.count(today_prefix) + 1
    
    return f"{prefix}-{today}-{count:03d}"

def detect_priority(message: str, error_msg: str = "") -> str:
    """自动检测优先级"""
    critical_keywords = ["崩溃", "数据丢失", "安全", "security", "crash", "data loss"]
    high_keywords = ["失败", "错误", "无法", "blocking", "failed", "error"]
    medium_keywords = ["优化", "改进", "建议", "improve", "optimize"]
    
    text = (message + " " + error_msg).lower()
    
    if any(kw in text for kw in critical_keywords):
        return "critical"
    elif any(kw in text for kw in high_keywords):
        return "high"
    elif any(kw in text for kw in medium_keywords):
        return "medium"
    return "low"

def detect_area(message: str) -> str:
    """自动检测影响区域"""
    area_keywords = {
        "config": ["配置", "config", "openclaw.json", "设置"],
        "infra": ["Gateway", "通道", "channel", "server", "部署"],
        "skills": ["技能", "skill", "能力", "功能"],
        "memory": ["记忆", "memory", "会话", "session"],
        "performance": ["性能", "performance", "速度", "优化"],
        "docs": ["文档", "doc", "说明", "readme"]
    }
    
    text = message.lower()
    for area, keywords in area_keywords.items():
        if any(kw in text for kw in keywords):
            return area
    return "general"

# ==================== 核心函数 ====================

def log_learning(message: str, category: str = "general", priority: Optional[str] = None, 
                 related_files: List[str] = None, pattern_key: Optional[str] = None) -> str:
    """记录学习条目"""
    entry_id = generate_id("learning")
    timestamp = datetime.now().isoformat()
    detected_priority = priority or detect_priority(message)
    area = detect_area(message)
    
    entry = f"""## [{entry_id}] {category}

**Logged**: {timestamp}
**Priority**: {detected_priority}
**Status**: pending
**Area**: {area}

### Summary
{message}

### Details
自动记录的学习条目，待补充详细上下文。

### Suggested Action
- [ ] 补充详细上下文
- [ ] 确定具体改进行动
- [ ] 评估是否需要促进到系统规则

### Metadata
- Source: auto-learn
- Related Files: {', '.join(related_files) if related_files else '待补充'}
- Tags: auto-generated, {category}
{f"- Pattern-Key: {pattern_key}" if pattern_key else ""}

---
"""
    
    file_path = LEARNINGS_DIR / "LEARNINGS.md"
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(entry + "\n")
    
    return entry_id

def log_error(command: str, error_msg: str, context: str = "") -> str:
    """记录错误条目"""
    entry_id = generate_id("error")
    timestamp = datetime.now().isoformat()
    priority = detect_priority("", error_msg)
    area = detect_area(command + " " + error_msg)
    
    entry = f"""## [{entry_id}] command_or_skill

**Logged**: {timestamp}
**Priority**: {priority}
**Status**: pending
**Area**: {area}

### Summary
命令执行失败：{command}

### Error
```
{error_msg}
```

### Context
{context if context else "自动记录，待补充详细上下文"}

### Suggested Fix
待分析

### Metadata
- Reproducible: unknown
- Related Files: 待补充

---
"""
    
    file_path = LEARNINGS_DIR / "ERRORS.md"
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(entry + "\n")
    
    return entry_id

def log_feature(request: str, user_context: str = "") -> str:
    """记录功能请求"""
    entry_id = generate_id("feature")
    timestamp = datetime.now().isoformat()
    
    entry = f"""## [{entry_id}] feature_name

**Logged**: {timestamp}
**Priority**: medium
**Status**: pending
**Area**: general

### Requested Capability
{request}

### User Context
{user_context if user_context else "自动记录，待补充"}

### Complexity Estimate
unknown

### Suggested Implementation
待评估

### Metadata
- Frequency: first_time

---
"""
    
    file_path = LEARNINGS_DIR / "FEATURE_REQUESTS.md"
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(entry + "\n")
    
    return entry_id

def review_learnings() -> Dict:
    """回顾待促进的学习"""
    results = {
        "total": 0,
        "pending": 0,
        "high_priority": [],
        "recurring": []
    }
    
    for file_name in ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"]:
        file_path = LEARNINGS_DIR / file_name
        if not file_path.exists():
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计
        all_entries = content.count("## [")
        pending = content.count("**Status**: pending")
        high_priority = content.count("**Priority**: high") + content.count("**Priority**: critical")
        
        results["total"] += all_entries
        results["pending"] += pending
        
        # 检测重复模式
        if "See Also" in content:
            see_also_count = content.count("**See Also**")
            if see_also_count > 0:
                results["recurring"].append({
                    "file": file_name,
                    "count": see_also_count
                })
    
    return results

def promote_to_memory(entry_id: str, target_file: str = "MEMORY.md") -> bool:
    """促进学习到系统记忆"""
    # 查找学习条目
    for file_name in ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"]:
        file_path = LEARNINGS_DIR / file_name
        if not file_path.exists():
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if entry_id in content:
            # 提取条目内容（简化版）
            start = content.find(f"## [{entry_id}]")
            if start == -1:
                continue
            
            # 找到下一个条目或文件末尾
            end = content.find("## [", start + 1)
            if end == -1:
                end = len(content)
            
            entry_content = content[start:end].strip()
            
            # 添加到目标文件
            target_path = WORKSPACE / target_file
            with open(target_path, 'a', encoding='utf-8') as f:
                f.write(f"\n\n## 学习条目 {entry_id}\n\n")
                f.write(f"*促进于 {datetime.now().strftime('%Y-%m-%d')}*\n\n")
                # 提取关键信息（简化处理）
                for line in entry_content.split('\n'):
                    if line.startswith("### Summary"):
                        continue
                    if line.startswith("## [") or line.startswith("**Logged**"):
                        continue
                    if line.strip() and not line.startswith("###"):
                        f.write(line + "\n")
            
            print(f"✅ 已促进 {entry_id} 到 {target_file}")
            return True
    
    print(f"❌ 未找到条目 {entry_id}")
    return False

# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description='🧠 自动学习记录器 - 傅盛三万风格',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 auto-learn.py --type learning --message "配置修改需要先备份"
  python3 auto-learn.py --type error --command "openclaw restart" --error "Invalid config"
  python3 auto-learn.py --type feature --request "自动日报发送"
  python3 auto-learn.py --review
        """
    )
    parser.add_argument('--type', choices=['learning', 'error', 'feature'], required=True)
    parser.add_argument('--message', type=str, help='学习内容（learning 类型）')
    parser.add_argument('--category', type=str, default='general', help='学习分类')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'], help='优先级')
    parser.add_argument('--command', type=str, help='失败的命令（error 类型）')
    parser.add_argument('--error', type=str, help='错误信息（error 类型）')
    parser.add_argument('--request', type=str, help='功能请求（feature 类型）')
    parser.add_argument('--context', type=str, help='上下文说明')
    parser.add_argument('--pattern-key', type=str, help='模式键（用于重复检测）')
    parser.add_argument('--review', action='store_true', help='回顾学习状态')
    parser.add_argument('--promote', type=str, help='促进条目到系统记忆（提供 entry_id）')
    
    args = parser.parse_args()
    
    print("🧠 自动学习记录器")
    print("=" * 60)
    print("核心理念：犯错 → 写规则 → 变 Skill → Never Again")
    print("=" * 60)
    
    if args.review:
        print("\n📊 学习状态回顾:\n")
        results = review_learnings()
        print(f"总条目数：{results['total']}")
        print(f"待处理：{results['pending']}")
        print(f"高优先级：{len(results['high_priority'])}")
        if results['recurring']:
            print(f"\n重复模式:")
            for r in results['recurring']:
                print(f"  - {r['file']}: {r['count']} 个关联条目")
        return
    
    if args.promote:
        print(f"\n📤 促进条目 {args.promote}...")
        promote_to_memory(args.promote)
        return
    
    if args.type == 'learning':
        if not args.message:
            print("❌ learning 类型需要 --message 参数")
            return
        
        entry_id = log_learning(
            args.message,
            category=args.category,
            priority=args.priority,
            pattern_key=args.pattern_key
        )
        print(f"✅ 已记录学习：{entry_id}")
        print(f"📁 文件：{LEARNINGS_DIR / 'LEARNINGS.md'}")
    
    elif args.type == 'error':
        if not args.command or not args.error:
            print("❌ error 类型需要 --command 和 --error 参数")
            return
        
        entry_id = log_error(args.command, args.error, args.context)
        print(f"✅ 已记录错误：{entry_id}")
        print(f"📁 文件：{LEARNINGS_DIR / 'ERRORS.md'}")
    
    elif args.type == 'feature':
        if not args.request:
            print("❌ feature 类型需要 --request 参数")
            return
        
        entry_id = log_feature(args.request, args.context)
        print(f"✅ 已记录功能请求：{entry_id}")
        print(f"📁 文件：{LEARNINGS_DIR / 'FEATURE_REQUESTS.md'}")
    
    print("\n💡 提示：使用 --review 查看学习状态，使用 --promote <entry_id> 促进到系统记忆")

if __name__ == "__main__":
    main()
