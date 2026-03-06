#!/usr/bin/env python3
"""
设置记忆归档定时任务
每周日 23:00 执行：
1. 归档 7 天前的日志到 memory/archive/
2. 扫描本周日志，提取模式更新 MEMORY.md
"""
import websocket
import json

GATEWAY_URL = "ws://localhost:14961"
TOKEN = "40c1dc3987f500cf2a80283d3f6ba725"

cron_job = {
    "name": "记忆归档与蒸馏",
    "schedule": {
        "kind": "cron",
        "expr": "0 23 * * 0",  # 每周日 23:00
        "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "message": """请执行记忆维护任务：

## 任务 1：归档旧日志
1. 检查 memory/ 目录下的所有日志文件
2. 将 7 天前的日志移动到 memory/archive/
3. 报告归档了哪些文件

## 任务 2：蒸馏本周记忆
1. 读取最近 7 天的日志 (memory/YYYY-MM-DD.md)
2. 提取以下模式：
   - 用户偏好变化
   - 重复出现的错误/教训
   - 新学到的技能/知识
3. 更新 MEMORY.md 添加新的长期记忆
4. 更新 TOOLS.md 添加新的配置/技巧

## 任务 3：清理临时文件
1. 删除 .tmp/ 目录下的所有文件
2. 报告清理结果

完成后通过 Feishu 发送总结报告。"""
    },
    "delivery": {
        "mode": "announce",
        "channel": "feishu"
    },
    "enabled": True
}

def on_message(ws, message):
    data = json.loads(message)
    
    if data.get('type') == 'event' and data.get('event') == 'connect.challenge':
        ws.send(json.dumps({
            'type': 'req',
            'method': 'connect',
            'params': {
                'minProtocol': 3,
                'maxProtocol': 3,
                'client': {'id': 'cli', 'version': 'dev', 'platform': 'python', 'mode': 'cli'},
                'role': 'operator',
                'scopes': ['operator.admin', 'operator.approvals', 'operator.pairing'],
                'auth': {'token': TOKEN}
            },
            'id': 'connect_1'
        }))
    
    elif data.get('id') == 'connect_1':
        if data.get('error'):
            print(f"连接失败：{data['error']}")
            ws.close()
        else:
            print("连接成功！添加记忆归档定时任务...")
            ws.send(json.dumps({
                'type': 'req',
                'method': 'cron.add',
                'params': {'job': cron_job},
                'id': 'add_cron_1'
            }))
    
    elif data.get('id') == 'add_cron_1':
        if data.get('error'):
            print(f"❌ 添加失败：{data.get('error')}")
        else:
            result = data.get('result', {})
            print(f"✅ 记忆归档定时任务已添加！")
            print(f"   任务 ID: {result.get('id')}")
            print(f"   执行时间：每周日 23:00")
        ws.close()

def on_error(ws, error):
    print(f"错误：{error}")

def on_close(ws, code, reason):
    print(f"连接关闭 (code={code})")

def on_open(ws):
    print("已连接到 Gateway")

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(GATEWAY_URL,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
