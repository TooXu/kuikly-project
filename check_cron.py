#!/usr/bin/env python3
import websocket
import json
import sys

GATEWAY_URL = "ws://localhost:14961"
TOKEN = "40c1dc3987f500cf2a80283d3f6ba725"

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
            print("连接成功！获取 cron 任务列表...")
            ws.send(json.dumps({
                'type': 'req',
                'method': 'cron.list',
                'params': {'includeDisabled': True},
                'id': 'list_cron_1'
            }))
    
    elif data.get('id') == 'list_cron_1':
        if data.get('error'):
            print(f"❌ 获取失败：{json.dumps(data.get('error'), ensure_ascii=False)}")
        else:
            print(f"✅ 成功！")
            jobs = data.get('result', {}).get('jobs', [])
            print(f"\n当前共有 {len(jobs)} 个定时任务:")
            for job in jobs:
                print(f"  - {job.get('name')}: {job.get('schedule', {}).get('expr')} (enabled={job.get('enabled')})")
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
