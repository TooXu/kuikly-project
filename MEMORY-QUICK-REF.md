# 🧠 记忆蒸馏快速参考

## 一键蒸馏
```bash
cd /home/admin/.openclaw
python3 workspace/scripts/memory-distill.py
```

## 查看定时任务
```bash
openclaw cron list
```

## 手动触发蒸馏任务
```bash
openclaw cron run <任务 ID>
```

## 文件位置
| 文件 | 路径 | 说明 |
|------|------|------|
| 蒸馏脚本 | `workspace/scripts/memory-distill.py` | 自动提取关键信息 |
| 长期记忆 | `workspace/MEMORY.md` | 3-10KB 精华 |
| 短期日志 | `workspace/memory/YYYY-MM-DD.md` | 保留 7 天 |
| 归档目录 | `workspace/memory/archive/` | 旧日志存储 |
| 使用指南 | `workspace/MEMORY-DISTILL-GUIDE.md` | 完整文档 |

## 检查清单 (每周)
- [ ] 蒸馏脚本已运行
- [ ] MEMORY.md 已更新
- [ ] 旧日志已归档
- [ ] MEMORY.md 大小 < 10KB

## 当前状态
- ✅ 定时任务：已激活 (每周日 23:00)
- ✅ 蒸馏脚本：已创建并测试
- ✅ HEARTBEAT.md：已添加记忆维护检查
- ✅ 归档目录：已启用

---
**创建日期**: 2026-03-04  
**下次蒸馏**: 2026-03-09 23:00
