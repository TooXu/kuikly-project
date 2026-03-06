#!/usr/bin/env python3
"""
设置每日19:00自动总结对话的定时任务
"""

import json
import websocket
import time
import sys

# Gateway配置
GATEWAY_URL = "ws://172.17.32.165:14961"
GATEWAY_TOKEN = "40c1dc3987f500cf2a80283d3f6ba725"

def add_daily_summary_cron():
    """添加每日总结定时任务"""
    
    # 构造cron任务
    cron_job = {
        "name": "Daily Conversation Summary",
        "schedule": {
            "kind": "cron",
            "expr": "0 19 * * *",  # 每天19:00 (UTC+8)
            "tz": "Asia/Shanghai"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "请总结今天的所有对话内容，包括用户发送的消息和你的回复，并通过Feishu发送给用户。"
        },
        "delivery": {
            "mode": "announce",
            "channel": "feishu"
        },
        "sessionTarget": "isolated",
        "enabled": True
    }
    
    try:
        # 连接到Gateway
        ws = websocket.WebSocket()
        ws.connect(GATEWAY_URL)
        
        # 发送认证
        auth_msg = {
            "method": "auth",
            "params": {"token": GATEWAY_TOKEN}
        }
        ws.send(json.dumps(auth_msg))
        
        # 等待认证响应
        response = ws.recv()
        auth_result = json.loads(response)
        
        if auth_result.get("error"):
            print(f"认证失败: {auth_result['error']}")
            return False
            
        # 添加cron任务
        cron_msg = {
            "method": "cron.add",
            "params": {"job": cron_job},
            "id": "add_cron_1"
        }
        ws.send(json.dumps(cron_msg))
        
        # 等待响应
        response = ws.recv()
        result = json.loads(response)
        
        if result.get("error"):
            print(f"添加定时任务失败: {result['error']}")
            return False
        else:
            print("✅ 每日对话总结定时任务已成功设置！")
            print("⏰ 每天19:00（北京时间）将自动执行")
            return True
            
    except Exception as e:
        print(f"连接Gateway失败: {e}")
        return False
    finally:
        try:
            ws.close()
        except:
            pass

if __name__ == "__main__":
    print("正在设置每日对话总结定时任务...")
    success = add_daily_summary_cron()
    if not success:
        print("❌ 设置失败，请检查Gateway服务状态")
        sys.exit(1)