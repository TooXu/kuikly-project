# HEARTBEAT.md - 定期检查任务

## 📊 日报系统检查 (每日)
- [ ] 验证日报生成：`python3 workspace/daily_report_pro.py --verbose`
- [ ] 检查日报保存：`workspace/daily-reports/daily-report-pro-YYYY-MM-DD.md`
- [ ] 确认 cron 任务正常执行

## 📰 AI 资讯日报 (新增 - 每日 9:00)
- [ ] 验证 AI 资讯生成：`python3 workspace/scripts/ai-news-daily.py`
- [ ] 检查资讯保存：`workspace/daily-reports/ai-news-daily-YYYY-MM-DD.md`
- [ ] 确认推送成功（Feishu/其他通道）

## 🔍 主动检查 (新增 - 每日 9:00)
- [ ] 运行主动检查：`python3 workspace/scripts/proactive-check.py --quick`
- [ ] 查看检查报告：`workspace/daily-reports/proactive-check-YYYY-MM-DD.md`
- [ ] 处理高优先级问题

## 🧠 技能沉淀 (新增 - 随时)
- [ ] 记录重要学习：`python3 workspace/scripts/auto-learn.py --type learning --message "..."`
- [ ] 记录错误：`python3 workspace/scripts/auto-learn.py --type error --command "..." --error "..."`
- [ ] 每周回顾：`python3 workspace/scripts/auto-learn.py --review`

## 记忆维护 (每周检查一次)
- [ ] 运行记忆蒸馏：`python3 workspace/scripts/memory-distill.py`
- [ ] 审查蒸馏结果，更新 MEMORY.md
- [ ] 确认 archive/ 目录正常归档

## 配置检查 (每月一次)
- [ ] 检查 openclaw.json 是否需要更新
- [ ] 验证插件版本是否为最新
- [ ] 审查已启用的通道是否正常

## 性能优化
- [ ] 检查日志文件大小，必要时清理
- [ ] 审查 cron 任务执行情况
- [ ] 检查 token 使用量

---
**最后检查**: 2026-03-06 (傅盛三万风格实现完成)
**下次检查**: 2026-03-07

## 📋 已实现功能（2026-03-06 更新）

### 实战日报系统 Pro（增强版）
- **脚本**: `workspace/daily_report_pro.py`
- **定时任务**: 每天 19:00 自动执行（cron）
- **灵感来源**: 《禅与龙虾养殖技术》
- **新增功能**:
  - 🎯 关键洞察提取
  - 📊 对话特征统计
  - 🧠 Skill 沉淀记录
  - 🔄 连续改进建议（Never Again）

### 自动学习记录器 ✨ 新增
- **脚本**: `workspace/scripts/auto-learn.py`
- **核心理念**: 犯错 → 写规则 → 变 Skill → Never Again
- **功能**:
  - 自动记录学习/错误/功能请求
  - 优先级自动检测
  - 区域自动分类
  - 模式键重复检测
  - 促进到系统记忆

### 主动检查器 ✨ 新增
- **脚本**: `workspace/scripts/proactive-check.py`
- **核心理念**: 主动发现问题，而不是被动等待
- **检查项目**:
  - Gateway 状态
  - 会话健康（上下文使用率）
  - 技能状态
  - 通道健康
  - 学习 backlog
  - 记忆文件状态
  - 磁盘使用

### 每日报告系统（基础版）
- **脚本**: `workspace/daily_report.py`
- **功能**: 基础日报生成

---
**参考**: `workspace/IMPLEMENTATION_SUMMARY.md` 完整实现文档
