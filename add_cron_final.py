#!/usr/bin/env python3
"""
使用正确的 Gateway 协议添加 cron 任务
"""
import websocket
import json
import hmac
import hashlib
import time
import sys

GATEWAY_URL = "ws://localhost:14961"
TOKEN = "40c1dc3987f500cf2a80283d3f6ba725"

cron_job = {
    "name": "每日对话总结",
    "schedule": {"kind": "cron", "expr": "0 19 * * *", "tz": "Asia/Shanghai"},
    "payload": {"kind": "agentTurn", "message": "请总结今天的所有对话内容，包括用户发送的消息和你的回复，并通过 Feishu 发送给用户。"},
    "delivery": {"mode": "announce", "channel": "feishu"},
    "sessionTarget": "isolated",
    "enabled": True
}

def on_message(ws, message):
    data = json.loads(message)
    print(f"收到：{json.dumps(data, indent=2, ensure_ascii=False)}")
    
    # 处理连接挑战 - 发送正确的 connect 请求
    if data.get('type') == 'event' and data.get('event') == 'connect.challenge':
        nonce = data['payload']['nonce']
        ts = data['payload']['ts']
        sig = hmac.new(TOKEN.encode(), f"{nonce}:{ts}".encode(), hashlib.sha256).hexdigest()
        
        print(f"发送 connect 请求...")
        # 正确的 connect 请求格式
        ws.send(json.dumps({
            'type': 'req',
            'method': 'connect',
            'params': {
                'minProtocol': 3,
                'maxProtocol': 3,
                'client': {
                    'id': 'cli',
                    'version': 'dev',
                    'platform': 'python',
                    'mode': 'cli'
                },
                'role': 'operator',
                'scopes': ['operator.admin', 'operator.approvals', 'operator.pairing'],
                'auth': {'token': TOKEN}
            },
            'id': 'connect_1'
        }))
    
    # connect 响应
    elif data.get('id') == 'connect_1':
        if data.get('error'):
            print(f"连接失败：{data['error']}")
            ws.close()
        else:
            print("连接成功！添加定时任务...")
            ws.send(json.dumps({
                'type': 'req',
                'method': 'cron.add',
                'params': {'job': cron_job},
                'id': 'add_cron_1'
            }))
    
    # cron.add 结果
    elif data.get('id') == 'add_cron_1':
        if data.get('error'):
            print(f"❌ 添加失败：{json.dumps(data.get('error'), ensure_ascii=False)}")
        else:
            print(f"✅ 成功！任务 ID: {data.get('result', {}).get('jobId')}")
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
