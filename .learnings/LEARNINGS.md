# Learnings Log

This file contains corrections, knowledge gaps, and best practices discovered during interactions.

---## [LRN-20260306-001] 配置规范

**Logged**: 2026-03-06T10:44:13.167253
**Priority**: high
**Status**: promoted
**Area**: config

### Summary
配置修改铁律：改前备份→查文档→改后双验证→再重启

### Details
**背景**: 2026-03-06 执行性能优化方案 A 时

**经过**:
1. ✅ 改前备份：`cp openclaw.json openclaw.json.backup.20260306-091020`
2. ❌ 未查文档：猜测 `compaction.mode: "aggressive"` 是有效值
3. ✅ 改后验证：JSON 格式验证通过
4. ❌ 重启失败：Gateway 报错 "Invalid input" for compaction.mode

**问题**: `compaction.mode` 有效值只有 `default` 和 `safeguard`，没有 `aggressive`

**结果**: 用户手动修改为 `compaction.mode: "default"`，其他优化生效

### Suggested Action
- [x] 补充详细上下文 ✅
- [x] 确定具体改进行动 ✅
- [x] 评估是否需要促进到系统规则 ✅

### Resolution
- **Promoted**: MEMORY.md (已在"🛡️ OpenClaw 配置修改铁律"章节)
- **Promoted At**: 2026-03-06
- **Notes**: 用户指定的 7 条配置修改铁律已存在于 MEMORY.md，本学习条目作为案例补充

### Metadata
- Source: auto-learn
- Related Files: /home/admin/.openclaw/openclaw.json, /home/admin/.openclaw/openclaw.json.backup.20260306-091020
- Tags: auto-generated, 配置规范，配置修改，性能优化
- Pattern-Key: config-change-iron-law
- See Also: MEMORY.md#openclaw-配置修改铁律

---

## [LRN-20260306-002] 学习记录规范

**Logged**: 2026-03-06T17:57:53.130332
**Priority**: medium
**Status**: promoted
**Area**: general

### Summary
学习条目描述必须准确，错误事实会误导未来决策

### Details
**背景**: 用户纠正 LRN-20260306-001 中的错误描述

**经过**:
1. LRN-20260306-001 中描述"Gateway 自动回滚为 compaction.mode: default"
2. 用户指出实际是"手动修改"而非"自动回滚"
3. 立即修正了错误描述
4. 记录此学习以确保未来准确性

**问题**: 学习条目的事实描述不准确，可能误导未来的决策和判断

**结果**: 
- ✅ 修正了 LRN-20260306-001 的描述
- ✅ 记录了此学习条目
- ✅ 促进到 AGENTS.md 作为行为规范

### Suggested Action
- [x] 补充详细上下文 ✅
- [x] 确定具体改进行动 ✅
- [x] 评估是否需要促进到系统规则 ✅

### Resolution
- **Promoted**: AGENTS.md (作为学习记录的行为规范)
- **Promoted At**: 2026-03-06
- **Notes**: 确保所有学习条目的描述准确，事实错误会误导未来决策

### Metadata
- Source: auto-learn
- Related Files: /home/admin/.openclaw/workspace/.learnings/LEARNINGS.md
- Tags: auto-generated, 学习记录规范，准确性，self-improving-agent
- Pattern-Key: learning-accuracy-important
- See Also: AGENTS.md#学习记录规范

---

