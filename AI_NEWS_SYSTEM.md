# 📰 AI 资讯日报系统

**创建日期**: 2026-03-06  
**灵感来源**: 用户需求 - 全网搜集 AI 相关资讯并每日推送

---

## 🎯 系统目标

自动搜集全网关于 **AI、模型、AI 编程、AI Agent、Skill、MCP** 的最新资讯，生成结构化日报，每日推送给用户。

---

## 📋 已实现功能

### 1️⃣ AI 资讯搜集脚本

**文件**: `workspace/scripts/ai-news-daily.py`

**搜索主题** (6 大主题，24 个搜索词):

| 主题 | 搜索词示例 |
|------|-----------|
| **AI 大模型** | GPT-5, Claude, Gemini, Llama, Mistral, Qwen |
| **AI Agent** | AI Agent 智能体，Autonomous Agent, LangChain, AutoGen |
| **AI 编程** | Copilot, Cursor, AI 代码生成，GitHub Copilot |
| **AI Skill/工具** | AI Skill, AI 插件，AI 工作流，AI 应用开发 |
| **MCP** | Model Context Protocol, AI 上下文协议，AI 互操作性 |
| **AI 行业资汛** | AI 融资，AI 政策，AI 会议，AI 创业 |

**功能**:
- ✅ 使用 SearXNG 隐私搜索引撃
- ✅ 每个主题最多 5 条新闻
- ✅ 自动去重（基于 URL）
- ✅ 生成结构化 Markdown 报告
- ✅ 包含趋势分析和明日关注

**使用方法**:
```bash
# 生成今日日报
python3 workspace/scripts/ai-news-daily.py

# 生成并推送
python3 workspace/scripts/ai-news-daily.py --send

# 详细输出
python3 workspace/scripts/ai-news-daily.py --verbose

# 测试模式（不保存）
python3 workspace/scripts/ai-news-daily.py --test
```

---

### 2️⃣ 定时任务配置

**文件**: `workspace/cron/ai-news-daily.json`

**执行时间**: 每日 9:00 (Asia/Shanghai)

**Cron 表达式**: `0 9 * * *`

**任务内容**:
```json
{
  "name": "AI 资讯日报",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "📰 AI 资讯日报时间到！运行：python3 .../ai-news-daily.py"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

---

### 3️⃣ 报告格式

**保存位置**: `workspace/daily-reports/ai-news-daily-YYYY-MM-DD.md`

**报告结构**:
```markdown
# 🤖 AI 资讯日报 - 2026-03-06

**生成时间**: 2026-03-06 09:00
**日期**: 2026-03-06 (Friday)
**数据来源**: SearXNG 全网搜索
**覆盖主题**: 6/6
**总文章数**: 30 篇

---

## 📰 今日热点
今日共搜集 **30** 篇相关文章，覆盖 **6** 个主题

## 📚 详细报道

### AI 大模型
1. **文章标题**
   - 来源：xxx
   - 时间：2026-03-06
   - 摘要：...
   - 链接：<url>

### AI Agent
...

## 🔍 趋势观察
- 🔥 最热门主题：AI 大模型 (5 篇)
- 📊 高频关键词：GPT(3), Agent(2), 开源 (2)

## 👀 明日关注
- 🔍 继续关注各大 AI 公司的最新动态
- 📅 留意 AI 会议和活动的最新公告
...
```

---

## 🧪 测试结果

**测试时间**: 2026-03-06 13:56

**测试结果**:
```
✅ 搜索主题：AI 大模型 - 5 条新闻
✅ 搜索主题：AI Agent - 5 条新闻
✅ 搜索主题：AI 编程 - 5 条新闻
✅ 搜索主题：AI Skill/工具 - 5 条新闻
✅ 搜索主题：MCP (Model Context Protocol) - 5 条新闻
✅ 搜索主题：AI 行业资汛 - 5 条新闻

总计：30 篇文章
覆盖主题：6/6
```

**报告预览**:
- 标题清晰
- 结构完整
- 链接可用
- 摘要简洁

---

## 📡 推送配置

### 当前状态
- [ ] Feishu 通道待配对
- [ ] Telegram 未配置
- [ ] 邮件推送未配置

### 推送方式（待配置）

#### 方式 1: Feishu（推荐）
```bash
# 需要完成 Feishu 通道配对后
python3 workspace/scripts/ai-news-daily.py --send
```

#### 方式 2: 邮件推送
```python
# 配置 SMTP 后
import smtplib
# 发送邮件逻辑
```

#### 方式 3: Webhook
```python
# 配置 Webhook URL 后
requests.post(WEBHOOK_URL, json={"content": report})
```

---

## 🔄 工作流程

```
每日 9:00 (Cron 触发)
     ↓
运行 ai-news-daily.py
     ↓
搜索 6 大主题（24 个搜索词）
     ↓
去重、筛选、排序
     ↓
生成 Markdown 报告
     ↓
保存到 daily-reports/
     ↓
推送到 Feishu/其他通道
     ↓
用户收到日报
```

---

## 📊 数据流

```
SearXNG API
     ↓
6 大主题 × 4 搜索词 = 24 次搜索
     ↓
最多 120 条原始结果
     ↓
去重 + 筛选
     ↓
最多 30 条精选文章
     ↓
结构化报告
```

---

## 🎯 优化建议

### 短期优化
1. ⚠️ **完成 Feishu 通道配对** - 实现自动推送
2. 📧 **配置邮件推送** - 备选推送方案
3. 🔔 **添加重要新闻即时通知** - 重大突破实时推送

### 中期优化
1. 📊 **个性化推荐** - 根据用户兴趣调整权重
2. 🗂️ **新闻分类归档** - 便于检索和回顾
3. 📈 **趋势分析增强** - 周报复盘、月度总结
4. 🤖 **AI 摘要生成** - 使用 LLM 生成更精准的摘要

### 长期优化
1. 🌐 **多语言支持** - 英文、中文等多语言资讯
2. 📱 **移动端适配** - 优化的手机阅读格式
3. 🔍 **高级搜索** - 按公司、人物、产品搜索
4. 📊 **数据可视化** - 趋势图表、热度图

---

## 🛠️ 文件清单

```
workspace/
├── scripts/
│   └── ai-news-daily.py          # AI 资讯搜集脚本 ✨ 新增
├── cron/
│   └── ai-news-daily.json        # 定时任务配置 ✨ 新增
├── daily-reports/
│   └── ai-news-daily-*.md        # 每日报告 ✨ 新增
└── AI_NEWS_SYSTEM.md             # 系统文档 ✨ 新增
```

---

## 📋 使用检查清单

### 每日检查（自动）
- [ ] 9:00 自动执行
- [ ] 报告生成成功
- [ ] 推送到用户

### 每周检查（手动）
- [ ] 检查搜索词是否需要更新
- [ ] 审查推送成功率
- [ ] 收集用户反馈

### 每月检查（手动）
- [ ] 优化搜索策略
- [ ] 更新搜索主题
- [ ] 评估推送渠道效果

---

## 💡 最佳实践

1. **搜索词优化**: 定期更新搜索词，保持资汛时效性
2. **去重策略**: 基于 URL 去重，避免重复内容
3. **摘要长度**: 控制在 150 字以内，保持简洁
4. **链接格式**: 使用 `<>` 包裹，避免 Feishu 嵌入预览
5. **推送时间**: 9:00 合适，用户开始工作时收到

---

## 🔧 故障排查

### 问题 1: 搜索失败
**症状**: 某主题无新闻
**原因**: SearXNG 服务不可用
**解决**: 检查 `SEARXNG_URL` 配置，确保服务运行

### 问题 2: 推送失败
**症状**: 报告生成但未收到
**原因**: 通道未配对或配置错误
**解决**: 完成 Feishu 通道配对，或配置其他推送方式

### 问题 3: 报告过大
**症状**: 消息发送失败
**原因**: 内容过长
**解决**: 减少 `max_results_per_topic` 或分段发送

---

## 📞 支持

**文档**: `workspace/AI_NEWS_SYSTEM.md`  
**脚本**: `workspace/scripts/ai-news-daily.py`  
**配置**: `workspace/cron/ai-news-daily.json`

---

*🤖 让 AI 帮你关注 AI 世界*  
*创建时间：2026-03-06*
