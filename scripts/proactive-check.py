#!/usr/bin/env python3
"""
🔍 主动检查器 - 傅盛三万风格
核心理念：像三万一样主动发现问题，而不是被动等待

功能：
- 定期检查系统健康状态
- 主动发现潜在问题
- 生成检查报告
- 支持定时任务集成

检查项目：
1. Gateway 状态
2. 会话内存使用
3. 技能状态
4. 通道健康
5. 待处理学习条目
6. 记忆文件状态

使用方法：
python3 proactive-check.py              # 完整检查
python3 proactive-check.py --quick      # 快速检查
python3 proactive-check.py --report     # 生成报告
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ==================== 配置区域 ====================
WORKSPACE = Path("/home/admin/.openclaw/workspace")
OPENCLAW_DIR = Path("/home/admin/.openclaw")
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = WORKSPACE / ".learnings"
SESSIONS_DIR = OPENCLAW_DIR / "agents" / "main" / "sessions"
REPORT_DIR = WORKSPACE / "daily-reports"

# 检查阈值
THRESHOLDS = {
    "session_context_warning_percent": 80,  # 80% 警告
    "session_context_critical_percent": 95,  # 95% 严重
    "memory_file_age_days": 7,  # 记忆文件保留天数
    "learning_pending_max": 10,  # 待处理学习最大数
    "disk_usage_warning": 80,  # 磁盘使用警告百分比
}

# ==================== 检查函数 ====================

def check_gateway_status() -> Dict:
    """检查 Gateway 状态"""
    result = {
        "name": "Gateway 状态",
        "status": "unknown",
        "issues": [],
        "details": {}
    }
    
    try:
        # 检查进程
        ps_result = subprocess.run(
            ["ps", "aux"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=5
        )
        
        if "openclaw-gateway" in ps_result.stdout:
            result["status"] = "running"
            
            # 检查日志中的错误
            log_dir = Path("/tmp/openclaw")
            today = date.today().strftime("%Y-%m-%d")
            log_file = log_dir / f"openclaw-{today}.log"
            
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_content = f.read()
                    if "error" in log_content.lower():
                        result["issues"].append("日志中发现错误记录")
                    if "pairing required" in log_content:
                        result["issues"].append("⚠️ Feishu 通道待配对")
        else:
            result["status"] = "not_running"
            result["issues"].append("🔴 Gateway 进程未运行")
    
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(f"检查失败：{str(e)}")
    
    return result

def check_session_health() -> Dict:
    """检查会话健康状态"""
    result = {
        "name": "会话健康",
        "status": "ok",
        "issues": [],
        "details": {
            "total_sessions": 0,
            "warning_sessions": [],
            "critical_sessions": []
        }
    }
    
    if not SESSIONS_DIR.exists():
        result["status"] = "unknown"
        return result
    
    try:
        sessions_file = SESSIONS_DIR / "sessions.json"
        if sessions_file.exists():
            with open(sessions_file, 'r', encoding='utf-8') as f:
                sessions = json.load(f)
            
            result["details"]["total_sessions"] = len(sessions)
            
            for key, session in sessions.items():
                input_tokens = session.get("inputTokens", 0)
                context_window = session.get("contextTokens", 262144)  # 默认 262k
                
                # 检查上下文使用率（基于 inputTokens / contextWindow）
                usage_percent = (input_tokens / context_window) * 100 if context_window > 0 else 0
                
                if usage_percent >= THRESHOLDS["session_context_critical_percent"]:
                    result["details"]["critical_sessions"].append({
                        "key": key,
                        "tokens": input_tokens,
                        "usage": f"{usage_percent:.1f}%"
                    })
                    result["status"] = "critical"
                    result["issues"].append(f"🔴 会话 {key.split(':')[-1][:8]}... 上下文爆满 ({usage_percent:.1f}%)")
                
                elif usage_percent >= THRESHOLDS["session_context_warning_percent"]:
                    result["details"]["warning_sessions"].append({
                        "key": key,
                        "tokens": input_tokens,
                        "usage": f"{usage_percent:.1f}%"
                    })
                    if result["status"] == "ok":
                        result["status"] = "warning"
                    result["issues"].append(f"⚠️ 会话 {key.split(':')[-1][:8]}... 上下文偏高 ({usage_percent:.1f}%)")
    
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(f"检查失败：{str(e)}")
    
    return result

def check_skills_status() -> Dict:
    """检查技能状态"""
    result = {
        "name": "技能状态",
        "status": "ok",
        "issues": [],
        "details": {
            "installed": [],
            "recommended_missing": []
        }
    }
    
    skills_dir = WORKSPACE / "skills"
    if not skills_dir.exists():
        result["status"] = "unknown"
        return result
    
    # 已安装技能
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            result["details"]["installed"].append(skill_dir.name)
    
    # 推荐技能（根据《禅与龙虾养殖技术》）
    recommended = ["searxng", "self-improving-agent", "github", "git", "summarize", "browser-automation"]
    for rec in recommended:
        if rec not in [s.replace("-", "_") for s in result["details"]["installed"]] and \
           rec not in result["details"]["installed"]:
            result["details"]["recommended_missing"].append(rec)
    
    if result["details"]["recommended_missing"]:
        result["status"] = "warning"
        result["issues"].append(f"⚠️ 缺少推荐技能：{', '.join(result['details']['recommended_missing'])}")
    
    return result

def check_channel_health() -> Dict:
    """检查通道健康状态"""
    result = {
        "name": "通道健康",
        "status": "ok",
        "issues": [],
        "details": {
            "feishu": "unknown",
            "telegram": "not_configured",
            "web_dashboard": "available"
        }
    }
    
    # 检查 openclaw.json
    config_file = OPENCLAW_DIR / "openclaw.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Feishu 状态
            if "channels" in config and "feishu" in config["channels"]:
                feishu_config = config["channels"]["feishu"]
                if feishu_config.get("enabled", False):
                    result["details"]["feishu"] = "enabled"
                    # 检查配对状态（简化）
                    if feishu_config.get("dmPolicy") == "pairing":
                        result["details"]["feishu"] = "pairing_required"
                        result["issues"].append("⚠️ Feishu 通道需要配对")
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"配置读取失败：{str(e)}")
    
    return result

def check_learning_backlog() -> Dict:
    """检查学习条目积压"""
    result = {
        "name": "学习 backlog",
        "status": "ok",
        "issues": [],
        "details": {
            "total": 0,
            "pending": 0,
            "high_priority": 0
        }
    }
    
    if not LEARNINGS_DIR.exists():
        return result
    
    for file_name in ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"]:
        file_path = LEARNINGS_DIR / file_name
        if not file_path.exists():
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            all_entries = content.count("## [")
            pending = content.count("**Status**: pending")
            high_priority = content.count("**Priority**: high") + content.count("**Priority**: critical")
            
            result["details"]["total"] += all_entries
            result["details"]["pending"] += pending
            result["details"]["high_priority"] += high_priority
        
        except:
            pass
    
    if result["details"]["pending"] > THRESHOLDS["learning_pending_max"]:
        result["status"] = "warning"
        result["issues"].append(f"⚠️ 待处理学习条目过多：{result['details']['pending']} 个")
    
    if result["details"]["high_priority"] > 0:
        result["status"] = "warning"
        result["issues"].append(f"🔴 高优先级待处理：{result['details']['high_priority']} 个")
    
    return result

def check_memory_files() -> Dict:
    """检查记忆文件状态"""
    result = {
        "name": "记忆文件",
        "status": "ok",
        "issues": [],
        "details": {
            "recent_files": [],
            "old_files": [],
            "missing_today": False
        }
    }
    
    if not MEMORY_DIR.exists():
        result["status"] = "unknown"
        return result
    
    today = date.today()
    
    # 检查今天和昨天的记忆文件
    for i in range(3):
        d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        f = MEMORY_DIR / f"{d}.md"
        if f.exists():
            result["details"]["recent_files"].append(d)
        elif i == 0:
            result["details"]["missing_today"] = True
            result["status"] = "warning"
            result["issues"].append("⚠️ 今日记忆文件缺失")
    
    # 检查旧文件（超过 7 天）
    try:
        for f in MEMORY_DIR.glob("*.md"):
            if f.stem != date.today().strftime("%Y-%m-%d"):
                try:
                    file_date = datetime.strptime(f.stem, "%Y-%m-%d").date()
                    age = (today - file_date).days
                    if age > THRESHOLDS["memory_file_age_days"]:
                        result["details"]["old_files"].append({
                            "file": f.name,
                            "age_days": age
                        })
                except:
                    pass
        
        if result["details"]["old_files"]:
            result["status"] = "warning"
            result["issues"].append(f"⚠️ {len(result['details']['old_files'])} 个记忆文件超过 7 天未归档")
    
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(f"检查失败：{str(e)}")
    
    return result

def check_disk_usage() -> Dict:
    """检查磁盘使用"""
    result = {
        "name": "磁盘使用",
        "status": "ok",
        "issues": [],
        "details": {}
    }
    
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        usage_percent = (used / total) * 100
        
        result["details"] = {
            "total_gb": total / (1024**3),
            "used_gb": used / (1024**3),
            "free_gb": free / (1024**3),
            "usage_percent": usage_percent
        }
        
        if usage_percent >= THRESHOLDS["disk_usage_warning"]:
            result["status"] = "warning"
            result["issues"].append(f"⚠️ 磁盘使用率偏高：{usage_percent:.1f}%")
    
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(f"检查失败：{str(e)}")
    
    return result

# ==================== 报告生成 ====================

def generate_check_report(checks: List[Dict]) -> str:
    """生成检查报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"# 🔍 OpenClaw 主动检查报告\n\n"
    report += f"**检查时间**: {timestamp}\n"
    report += f"**检查项目**: {len(checks)} 项\n\n"
    
    # 总体状态
    critical_count = sum(1 for c in checks if c["status"] == "critical")
    warning_count = sum(1 for c in checks if c["status"] == "warning")
    ok_count = sum(1 for c in checks if c["status"] == "ok")
    
    overall_status = "🟢 健康" if critical_count == 0 and warning_count == 0 else \
                     "🔴 严重" if critical_count > 0 else "🟡 警告"
    
    report += f"**总体状态**: {overall_status}\n\n"
    report += f"| 状态 | 数量 |\n|------|------|\n"
    report += f"| 🟢 正常 | {ok_count} |\n"
    report += f"| 🟡 警告 | {warning_count} |\n"
    report += f"| 🔴 严重 | {critical_count} |\n\n"
    report += "---\n\n"
    
    # 详细检查结果
    report += "## 📋 详细检查\n\n"
    
    for check in checks:
        status_emoji = {"ok": "✅", "warning": "⚠️", "critical": "🔴", "error": "❌", "unknown": "❓"}.get(check["status"], "❓")
        report += f"### {status_emoji} {check['name']}\n\n"
        
        if check["issues"]:
            for issue in check["issues"]:
                report += f"- {issue}\n"
        else:
            report += "- ✅ 无异常\n"
        
        report += "\n"
    
    # 建议行动
    report += "## 🎯 建议行动\n\n"
    
    actions = []
    for check in checks:
        if check["status"] == "critical":
            actions.append(f"🔴 **立即处理**: {check['name']} - {check['issues'][0] if check['issues'] else '严重问题'}")
        elif check["status"] == "warning":
            actions.append(f"⚠️ **尽快处理**: {check['name']} - {check['issues'][0] if check['issues'] else '需要注意'}")
    
    if not actions:
        actions.append("✅ 系统运行正常，无需特别操作")
    
    for action in actions:
        report += f"- {action}\n"
    
    report += "\n---\n\n"
    report += f"*🤖 此报告由 OpenClaw 主动检查器自动生成*\n"
    report += f"*灵感来源：傅盛三万的主动关怀能力*\n"
    
    return report

def save_report(report: str) -> Path:
    """保存报告"""
    today = date.today().strftime("%Y-%m-%d")
    REPORT_DIR.mkdir(exist_ok=True)
    report_file = REPORT_DIR / f"proactive-check-{today}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📄 报告已保存：{report_file.absolute()}")
    return report_file

def send_to_feishu_as_file(report_file: Path) -> bool:
    """以文件形式发送到 Feishu"""
    import subprocess
    
    print(f"📤 准备发送文件到 Feishu: {report_file.name}")
    
    try:
        # 调用 Feishu 文件发送脚本
        cmd = [
            'python3',
            '/home/admin/.openclaw/workspace/scripts/feishu-send-file.py',
            str(report_file.absolute()),
            f'🔍 主动检查报告 - {report_file.stem.split("-")[-1]}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "✅ 文件发送完成" in result.stdout:
            print(f"✅ 文件已发送到 Feishu")
            return True
        else:
            print(f"❌ 发送失败：{result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ 发送错误：{str(e)}")
        return False

# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description='🔍 OpenClaw 主动检查器 - 傅盛三万风格'
    )
    parser.add_argument('--quick', action='store_true', help='快速检查（仅关键项目）')
    parser.add_argument('--report', action='store_true', help='生成完整报告')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--send', action='store_true', help='以文件形式发送到 Feishu')
    args = parser.parse_args()
    
    print("🔍 OpenClaw 主动检查器")
    print("=" * 60)
    print("核心理念：主动发现问题，而不是被动等待")
    print("=" * 60)
    
    # 执行检查
    checks = []
    
    # 必检项目
    checks.append(check_gateway_status())
    checks.append(check_session_health())
    
    if not args.quick:
        checks.append(check_skills_status())
        checks.append(check_channel_health())
        checks.append(check_learning_backlog())
        checks.append(check_memory_files())
        checks.append(check_disk_usage())
    
    # 输出
    if args.json:
        print(json.dumps(checks, indent=2, ensure_ascii=False))
    else:
        print("\n📊 检查结果:\n")
        for check in checks:
            status_emoji = {"ok": "✅", "warning": "⚠️", "critical": "🔴", "error": "❌", "unknown": "❓"}.get(check["status"], "❓")
            print(f"{status_emoji} {check['name']}: {check['status']}")
            if check["issues"]:
                for issue in check["issues"]:
                    print(f"   {issue}")
    
    # 生成报告
    if args.report:
        print("\n📝 生成报告...")
        report = generate_check_report(checks)
        report_file = save_report(report)
        
        # 发送文件（可选）
        if args.send:
            if send_to_feishu_as_file(report_file):
                print("✅ 已发送到 Feishu（文件形式）")
            else:
                print("❌ 发送失败")
        
        # 显示报告预览
        print("\n" + "=" * 60)
        print("报告预览（前 1000 字符）:")
        print("=" * 60)
        print(report[:1000] + "..." if len(report) > 1000 else report)

if __name__ == "__main__":
    main()
