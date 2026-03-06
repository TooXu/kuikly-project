#!/usr/bin/env python3
"""
📰 AI 资讯日报生成器
功能：全网搜集 AI、模型、AI 编程、AI Agent、Skill、MCP 相关资汛，生成日报

使用方法：
python3 ai-news-daily.py              # 生成今日日报
python3 ai-news-daily.py --send       # 生成并推送
python3 ai-news-daily.py --verbose    # 详细输出
"""

import os
import sys
import json
import requests
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ==================== 配置区域 ====================
WORKSPACE = Path("/home/admin/.openclaw/workspace")
REPORT_DIR = WORKSPACE / "daily-reports"
MEMORY_DIR = WORKSPACE / "memory"

# SearXNG 配置
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")

# 搜索主题配置（优化版 - 精准搜索词 + 排除词）
SEARCH_TOPICS = {
    "AI 大模型": [
        "OpenAI GPT-5 发布 2026",
        "Claude 3.5 Anthropic 新模型",
        "Gemini 2.0 Google AI",
        "Qwen2.5 阿里通义千问",
        "LLM 大模型 性能评测 2026"
    ],
    "AI Agent": [
        "AI Agent 智能体 企业应用",
        "Autonomous Agent 自主代理 框架",
        "LangChain AutoGen 多 Agent",
        "AI Agent 工作流 自动化",
        "Agent 编排 任务规划"
    ],
    "AI 编程": [
        "GitHub Copilot 新功能 2026",
        "Cursor AI IDE 更新",
        "AI 代码生成 辅助编程",
        " Devin AI 软件工程师",
        "AI 编程工具 效率提升"
    ],
    "AI Skill/工具": [
        "AI 工具集 技能市场",
        "AI 插件 生态系统",
        "AI 工作流 自动化平台",
        "n8n Zapier AI 集成",
        "AI API 开发者工具"
    ],
    "MCP (Model Context Protocol)": [
        "MCP Model Context Protocol Anthropic",
        "AI 上下文协议 标准",
        "AI 互操作性 协议",
        "Model Context Protocol 实现"
    ],
    "AI 行业资汛": [
        "AI 公司 融资 2026",
        "AI 政策 监管 法规 最新",
        "AI 会议 MWC CES 2026",
        "AI 创业 新产品 发布",
        "AI 投资 并购 动态"
    ]
}

# 排除的低质量来源
EXCLUDE_SOURCES = [
    "jingyan.baidu.com",  # 百度经验
    "zhidao.baidu.com",   # 百度知道
    "tieba.baidu.com",    # 百度贴吧
    "wenku.baidu.com",    # 百度文库
    "experience.baidu.com",
]

# 高质量来源优先
PRIORITY_SOURCES = [
    "github.com",
    "arxiv.org",
    "huggingface.co",
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "reuters.com",
    "bloomberg.com",
    "36kr.com",
    "huxiu.com",
    "qbitai.com",
    "机器之心",
    "量子位",
]

# 日报配置
REPORT_CONFIG = {
    "title": "🤖 AI 资讯日报",
    "max_results_per_topic": 5,  # 每个主题最多保留的结果数
    "min_relevance_score": 0.3,  # 最低相关性分数
}

# ==================== 搜索函数 ====================

def search_searxng(query: str, num_results: int = 10, time_range: str = "day") -> List[Dict]:
    """使用 SearXNG 搜索（优化版 - 过滤低质量内容）"""
    try:
        url = f"{SEARXNG_URL}/search"
        params = {
            "q": query,
            "format": "json",
            "pageno": 1,
            "language": "zh-CN",
            "time_range": time_range
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for item in data.get("results", []):
            url = item.get("url", "")
            
            # 过滤低质量来源
            if any(exclude in url for exclude in EXCLUDE_SOURCES):
                continue
            
            # 过滤过时的内容（检查 URL 或标题中的日期）
            title = item.get("title", "")
            if "2024" in title or "2023" in title or "2022" in title:
                if "2026" not in title and "2025" not in title:
                    continue
            
            results.append({
                "title": title,
                "url": url,
                "content": item.get("content", "")[:150],  # 限制内容长度
                "source": url.split('/')[2] if 'url' in item else "",
                "publishedDate": item.get("publishedDate", ""),
                "category": item.get("category", "general"),
                "score": calculate_relevance_score(item, query)
            })
        
        # 按相关性排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:num_results]
    
    except Exception as e:
        print(f"⚠️ 搜索失败 '{query}': {str(e)}")
        return []

def calculate_relevance_score(item: Dict, query: str) -> float:
    """计算内容相关性分数"""
    score = 0.0
    
    title = item.get("title", "").lower()
    content = item.get("content", "").lower()
    url = item.get("url", "").lower()
    
    # 高质量来源加分
    for source in PRIORITY_SOURCES:
        if source in url:
            score += 2.0
            break
    
    # 标题包含关键词加分
    query_words = query.lower().split()
    for word in query_words:
        if len(word) > 2:  # 忽略短词
            if word in title:
                score += 1.5
            elif word in content:
                score += 0.5
    
    # 有时效性关键词加分
    if "2026" in title or "最新" in title or "发布" in title:
        score += 1.0
    
    # 有发布日期加分
    if item.get("publishedDate"):
        score += 0.5
    
    return score

def search_all_topics() -> Dict[str, List[Dict]]:
    """搜索所有主题"""
    all_news = {}
    
    for topic, queries in SEARCH_TOPICS.items():
        print(f"🔍 搜索主题：{topic}")
        topic_results = []
        
        for query in queries:
            results = search_searxng(query, num_results=5, time_range="day")
            topic_results.extend(results)
        
        # 去重（基于 URL）
        seen_urls = set()
        unique_results = []
        for r in topic_results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique_results.append(r)
        
        # 限制结果数量
        all_news[topic] = unique_results[:REPORT_CONFIG["max_results_per_topic"]]
        print(f"   ✅ 找到 {len(all_news[topic])} 条相关新闻")
    
    return all_news

# ==================== 报告生成函数 ====================

def generate_news_summary(news: Dict[str, List[Dict]]) -> str:
    """生成新闻摘要（优化版 - 更简洁、更专业）"""
    report = ""
    
    for topic, articles in news.items():
        if not articles:
            continue
        
        report += f"\n### {topic}\n\n"
        
        for i, article in enumerate(articles, 1):
            # 标题 + 来源
            source = article.get('source', '未知来源')
            if not source:
                source = article['url'].split('/')[2] if 'url' in article else '未知来源'
            
            # 精简标题（去除冗余）
            title = article['title']
            if len(title) > 60:
                title = title[:57] + "..."
            
            report += f"**{i}. {title}**\n"
            report += f"📰 {source}"
            
            # 发布时间（如果有）
            if article.get("publishedDate"):
                report += f" · {article['publishedDate'][:10]}"
            report += "\n"
            
            # 摘要/看点（精简到 80 字）
            if article.get("content"):
                content = article['content'].replace('\n', ' ').strip()
                # 清理 HTML 标签和多余空格
                content = ' '.join(content.split())
                if len(content) > 80:
                    content = content[:77] + "..."
                report += f"💡 {content}\n"
            
            # 原文链接
            report += f"🔗 {article['url']}\n\n"
    
    return report

def generate_daily_report(news: Dict[str, List[Dict]]) -> str:
    """生成完整日报（简洁格式）"""
    today = date.today().strftime("%Y-%m-%d")
    weekday_en = date.today().strftime("%A")
    weekday_map = {"Monday": "周一", "Tuesday": "周二", "Wednesday": "周三", 
                   "Thursday": "周四", "Friday": "周五", "Saturday": "周六", "Sunday": "周日"}
    weekday = weekday_map.get(weekday_en, "")
    generation_time = datetime.now().strftime("%H:%M")
    
    # 统计
    total_articles = sum(len(articles) for articles in news.values())
    topics_with_news = sum(1 for articles in news.values() if articles)
    
    # 头部
    report = f"📢【AI 业界资讯 · {today}】\n\n"
    report += f"**生成时间**: {generation_time} | **来源**: SearXNG 全网搜索\n"
    report += f"**覆盖**: {topics_with_news}/{len(SEARCH_TOPICS)} 主题 | **总计**: {total_articles} 篇\n\n"
    report += "---\n\n"
    
    # 详细新闻
    news_content = generate_news_summary(news)
    report += news_content if news_content else "*今日暂无内容*\n"
    
    # 趋势观察
    if total_articles > 0:
        report += "\n---\n\n"
        report += "## 🔍 趋势观察\n\n"
        report += generate_trend_analysis(news)
    
    # 页脚
    report += "\n---\n"
    report += f"*🤖 OpenClaw AI 资讯系统自动生成 | 下次推送：明日 9:00*\n"
    
    return report

def generate_trend_analysis(news: Dict[str, List[Dict]]) -> str:
    """生成趋势分析"""
    trends = []
    
    # 分析哪个主题最活跃
    topic_counts = {topic: len(articles) for topic, articles in news.items()}
    if topic_counts:
        hottest_topic = max(topic_counts, key=topic_counts.get)
        hottest_count = topic_counts[hottest_topic]
        trends.append(f"🔥 **最热门主题**: {hottest_topic} ({hottest_count} 篇)")
    
    # 分析高频关键词
    all_titles = []
    for articles in news.values():
        for article in articles:
            all_titles.append(article.get("title", "").lower())
    
    keywords = ["GPT", "Claude", "Agent", "开源", "发布", "更新", "新"]
    keyword_counts = {kw: sum(1 for t in all_titles if kw.lower() in t) for kw in keywords}
    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    if top_keywords and top_keywords[0][1] > 0:
        kw_list = ", ".join([f"{kw}({count})" for kw, count in top_keywords if count > 0])
        trends.append(f"📊 **高频关键词**: {kw_list}")
    
    if trends:
        return "\n".join([f"- {t}" for t in trends]) + "\n"
    else:
        return "*数据不足，无法生成趋势分析*\n"

def generate_tomorrow_watch() -> str:
    """生成明日关注"""
    watches = [
        "🔍 继续关注各大 AI 公司的最新动态",
        "📅 留意 AI 会议和活动的最新公告",
        "💻 关注开源 AI 项目的更新",
        "🤖 跟踪 AI Agent 领域的最新进展"
    ]
    
    return "\n".join([f"- {w}" for w in watches]) + "\n"

def save_report(report: str) -> Path:
    """保存报告"""
    today = date.today().strftime("%Y-%m-%d")
    REPORT_DIR.mkdir(exist_ok=True)
    report_file = REPORT_DIR / f"ai-news-daily-{today}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_file

def send_to_feishu(report_file: Path) -> bool:
    """发送到 Feishu（文件形式）"""
    import subprocess
    
    print(f"📤 准备发送文件到 Feishu: {report_file.name}")
    
    try:
        # 调用 Feishu 文件发送脚本
        cmd = [
            'python3',
            '/home/admin/.openclaw/workspace/scripts/feishu-send-file.py',
            str(report_file.absolute()),
            f'📰 AI 资讯日报 - {report_file.stem.split("-")[-1]}'
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
    import argparse
    parser = argparse.ArgumentParser(description='📰 AI 资讯日报生成器')
    parser.add_argument('--send', action='store_true', help='发送到 Feishu')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    parser.add_argument('--test', action='store_true', help='测试模式（不保存）')
    args = parser.parse_args()
    
    print("📰 AI 资讯日报生成器")
    print("=" * 60)
    print("搜索主题:", ", ".join(SEARCH_TOPICS.keys()))
    print("=" * 60)
    
    # 收集新闻
    print("\n🔍 开始搜索全网资讯...")
    news = search_all_topics()
    
    # 生成报告
    print("\n📝 正在生成日报...")
    report = generate_daily_report(news)
    
    if args.test:
        print("\n✅ 测试模式：报告生成成功（未保存）")
        print("\n" + "=" * 60)
        print("报告预览（前 1500 字符）:")
        print("=" * 60)
        print(report[:1500] + "...")
        return
    
    # 保存报告
    if not args.test:
        report_file = save_report(report)
        print(f"✅ 报告已保存：{report_file}")
    
    # 发送（可选）
    if args.send:
        if send_to_feishu(report_file):
            print("✅ 已发送到 Feishu")
        else:
            print("❌ 发送失败")
    
    # 预览
    print("\n" + "=" * 60)
    print("报告预览（前 1500 字符）:")
    print("=" * 60)
    print(report[:1500] + "...")
    print("=" * 60)
    print("✅ AI 资讯日报生成完成！")

if __name__ == "__main__":
    main()
