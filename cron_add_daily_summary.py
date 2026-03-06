#!/usr/bin/env python3
"""
根据官方文档正确添加 cron 任务
"""
import websocket
import json
import hmac
import hashlib

GATEWAY_URL = "ws://localhost:14961"
TOKEN = "40c1dc3987f500cf2a80283d3f6ba725"

# 根据官方文档的正确格式
cron_job = {
    "name": "每日对话总结",
    "schedule": {
        "kind": "cron",
        "expr": "0 19 * * *",
        "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "message": "请总结今天的所有对话内容，包括用户发送的消息和你的回复，并通过 Feishu 发送给用户。"
    },
    "delivery": {
        "mode": "announce",
        "channel": "feishu"
    },
    "enabled": True
}

def on_message(ws, message):
    data = json.loads(message)
    print(f"收到：{json.dumps(data, indent=2, ensure_ascii=False)}")
    
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
            print("连接成功！先删除旧任务（如果存在）...")
            # 先删除旧任务
            ws.send(json.dumps({
                'type': 'req',
                'method': 'cron.remove',
                'params': {'jobId': '69bc95bf-54a1-4c01-ba87-8a9a5dc2dd78'},
                'id': 'remove_old_1'
            }))
    
    elif data.get('id') == 'remove_old_1':
        print("旧任务已删除（或不存在），添加新任务...")
        ws.send(json.dumps({
            'type': 'req',
            'method': 'cron.add',
            'params': {'job': cron_job},
            'id': 'add_cron_1'
        }))
    
    elif data.get('id') == 'add_cron_1':
        if data.get('error'):
            print(f"❌ 添加失败：{json.dumps(data.get('error'), ensure_ascii=False)}")
        else:
            result = data.get('result', {})
            print(f"✅ 成功！")
            print(f"任务 ID: {result.get('id')}")
            print(f"名称：{result.get('name')}")
            print(f" schedule: {result.get('schedule')}")
            print(f"下次运行：{result.get('state', {}).get('nextRunAtMs')}")
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
