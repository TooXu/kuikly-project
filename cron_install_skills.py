#!/usr/bin/env python3
"""
设置 1 小时后尝试安装技能的定时任务
"""
import websocket
import json
from datetime import datetime, timedelta

GATEWAY_URL = "ws://localhost:14961"
TOKEN = "40c1dc3987f500cf2a80283d3f6ba725"

# 1 小时后的时间（UTC）
run_time = datetime.utcnow() + timedelta(hours=1)
at_time = run_time.strftime("%Y-%m-%dT%H:%M:%SZ")

cron_job = {
    "name": "安装 ClawHub 技能",
    "schedule": {
        "kind": "at",
        "at": at_time
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "message": f"""尝试安装以下 ClawHub 技能：
1. openclaw-skill-vetter (安全扫描)
2. summarize (文档总结)

安装命令：
```bash
cd /home/admin/.openclaw/workspace
clawhub install openclaw-skill-vetter
clawhub install summarize
```

如果遇到速率限制 (Rate limit exceeded)：
- 告知用户当前限制状态
- 创建新的定时任务，延迟 1-2 小时后再试
- 直到所有技能都安装成功

安装完成后通过 Feishu 通知用户结果。"""
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
            print(f"连接成功！添加定时任务：{at_time}")
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
            print(f"✅ 定时任务已添加！")
            print(f"   任务 ID: {result.get('id')}")
            print(f"   执行时间：{at_time}")
            print(f"   任务名称：{result.get('name')}")
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
