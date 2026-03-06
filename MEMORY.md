## 👤 用户信息

- **称呼**: 老板
- **职位**: 移动端 App 开发技术负责人
- **交流风格**: 金字塔原理（结论先行，以上统下）

## 🔧 工具与配置规则

1. **联网搜索**: 优先使用 searxng skill
2. **OpenClaw 配置/功能**: 任何与 OpenClaw 或自身配置、功能相关的需求和改动，**优先到官方文档 https://docs.openclaw.ai/ 进行搜索查找**，确认正确用法后再操作
3. **速率限制处理**: 遇到 API 速率限制时，告知用户并建议等待，不要连续重试
4. **性能优化**: 长时间操作前告知预计耗时，失败 2 次后放弃并提供替代方案
5. **ClawHub 安装技能**: 国内访问受限，需等待速率限制解除（约 5-10 分钟/次）或使用代理

## 🧠 记忆蒸馏流程（2026-03-04 优化）

### 自动蒸馏
- **频率**: 每周日 23:00 自动执行
- **脚本**: `workspace/scripts/memory-distill.py`
- **功能**: 提取关键信息、归档 7 天前日志、生成 MEMORY.md 更新建议
- **定时任务**: 已配置 cron 任务 (每周日 23:00)

### 记忆层级
- **MEMORY.md**: 长期记忆 (3-10KB)，永久保留
- **memory/YYYY-MM-DD.md**: 短期日志，保留 7 天
- **memory/archive/**: 归档目录，存储 7 天前日志

### 手动蒸馏命令
```bash
cd /home/admin/.openclaw
python3 workspace/scripts/memory-distill.py
```

### 提取模式
- ✅ 决策、教训、偏好、技能、配置更新
- ❌ 临时对话、琐事、重复信息

---

## 🛡️ OpenClaw 配置修改铁律（用户指定）

### 1. openclaw.json 修改三步铁律
- ✅ **改前备份**（带时间戳）
- ✅ **改前查文档**确认字段合法值
- ✅ **改后双验证**（JSON 解析 + `openclaw doctor`）通过后才能重启

### 2. 禁止危险重启动作
- ❌ 禁止先 kill 前台 gateway 再 systemd start
- ❌ 禁止 stop+start 快速连击
- ✅ 优先 restart，并在校验通过后执行

### 3. 禁止猜命令/猜配置
- ✅ 不熟悉命令先查文档或 `--help`
- ✅ 配置字段不靠猜，必须按 schema

### 4. 给选项后必须等确认
- ✅ 不可擅自拍板执行未确认的方案

### 5. 密钥安全铁律
- ✅ 不在输出里暴露任何密钥
- ✅ 所有密钥通过 1Password op 读取
- ✅ 示例里只用占位符，不写真值

### 6. 1Password SSH 调用铁律（强制）
- ✅ 所有 op 相关操作必须在 tmux 里跑
- ✅ 私钥只进 ssh-agent，不落盘
- ✅ 连接服务器统一走 1P op 取密钥

### 7. 代码/生产变更流程
- ✅ 本地改→测试→commit→用户确认→再推送/部署
- ✅ 不直接在线服务器改核心代码

---

## 📊 已实现功能（2026-03-05）

### 实战日报系统 Pro（增强版）
- **脚本**: `workspace/daily_report_pro.py`
- **定时任务**: 每天 19:00 自动执行（cron）
- **灵感来源**: 《禅与龙虾养殖技术》
- **功能**:
  - 自动读取记忆文件
  - 统计技能使用情况
  - 记录 Gateway 状态和通道健康
  - 生成趋势分析（7 天活跃度）
  - 提供明日建议
- **报告保存**: `workspace/daily-reports/daily-report-pro-YYYY-MM-DD.md`
- **核心理念**: 龙虾不是聊天机器人，是 24 小时干活的 Agent

### 每日报告系统（基础版）
- **脚本**: `workspace/daily_report.py`
- **功能**: 基础日报生成

### 已安装技能
- searxng (1.0.3) - 联网搜索
- self-improving-agent (1.0.11) - 自我改进
- github (1.0.0) - GitHub 操作
- git (1.0.7) - Git 版本控制

### 待安装技能
- summarize - 文档摘要
- browser-automation - 浏览器自动化
- skill-creator - 技能创建器

### 待解决问题
- Feishu 通道配对（Dashboard: http://172.17.32.165:14961/）

