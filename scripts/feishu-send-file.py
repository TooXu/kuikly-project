#!/usr/bin/env python3
"""
📤 Feishu 文件发送脚本
使用 Feishu SDK 直接发送文件到飞书

依赖：
pip install @larksuiteoapi/node-sdk (或使用 requests 调用 API)

使用方法：
python3 feishu-send-file.py <文件路径> [消息文本]
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
from datetime import datetime

# ==================== 配置区域 ====================
# Feishu 应用配置（从 openclaw.json 读取或环境变量）
APP_ID = os.getenv("FEISHU_APP_ID", "cli_a91518f8c6391bc8")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "y54Ac7b0zIoBjkgEEbOWgck5jJKYWTTF")

# 接收者配置
USER_OPEN_ID = "ou_f444552b96595ae88251e9988ceb85b7"

# Feishu API 端点
FEISHU_TENANT_ACCESS_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_UPLOAD_FILE_URL = "https://open.feishu.cn/open-apis/im/v1/files"
FEISHU_SEND_MESSAGE_URL = "https://open.feishu.cn/open-apis/im/v1/messages"

# ==================== 辅助函数 ====================

def get_tenant_access_token():
    """获取飞书 tenant_access_token"""
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    response = requests.post(FEISHU_TENANT_ACCESS_TOKEN_URL, json=payload)
    result = response.json()
    
    if result.get("code") != 0:
        raise Exception(f"获取 access_token 失败：{result}")
    
    return result["tenant_access_token"]

def upload_file(token: str, file_path: Path):
    """上传文件到飞书"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 根据文件扩展名选择正确的文件类型
    file_ext = file_path.suffix.lower()
    file_type_map = {
        ".md": "doc",
        ".txt": "doc",
        ".pdf": "pdf",
        ".doc": "doc",
        ".docx": "doc",
        ".xls": "xls",
        ".xlsx": "xls",
        ".ppt": "ppt",
        ".pptx": "ppt",
        ".jpg": "image",
        ".png": "image",
        ".gif": "image",
    }
    file_type = file_type_map.get(file_ext, "stream")
    
    # 准备文件
    files = {
        "file": (file_path.name, open(file_path, "rb"), "application/octet-stream")
    }
    
    data = {
        "file_type": file_type
    }
    
    response = requests.post(FEISHU_UPLOAD_FILE_URL, headers=headers, files=files, data=data)
    result = response.json()
    
    if result.get("code") != 0:
        raise Exception(f"上传文件失败：{result}")
    
    file_key = result["data"]["file_key"]
    file_url = result["data"].get("file_url", "")
    
    print(f"✅ 文件上传成功：{file_path.name}")
    print(f"   File Key: {file_key}")
    if file_url:
        print(f"   File URL: {file_url}")
    
    return file_key, file_url

def send_file_message(token: str, user_open_id: str, file_key: str, file_name: str, file_url: str = "", text: str = ""):
    """发送文件消息（使用正确的飞书文件格式）"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 使用飞书原生文件消息格式
    # 参考：https://open.feishu.cn/document/server-docs/im-v1/message/create
    content = {
        "file_key": file_key,
        "file_name": file_name
    }
    
    # 如果有说明文字，添加到文件名后面
    if text:
        content["file_name"] = f"{file_name}\n\n{text}"
    
    payload = {
        "receive_id": user_open_id,
        "msg_type": "file",
        "content": json.dumps(content)
    }
    
    params = {
        "receive_id_type": "open_id"
    }
    
    response = requests.post(FEISHU_SEND_MESSAGE_URL, headers=headers, json=payload, params=params)
    result = response.json()
    
    if result.get("code") != 0:
        raise Exception(f"发送消息失败：{result}")
    
    message_id = result["data"]["message_id"]
    print(f"✅ 消息发送成功：{message_id}")
    
    return message_id

# ==================== 主函数 ====================

def main():
    if len(sys.argv) < 2:
        print("❌ 用法：python3 feishu-send-file.py <文件路径> [消息文本]")
        print("\n示例:")
        print("  python3 feishu-send-file.py /path/to/file.md")
        print("  python3 feishu-send-file.py /path/to/file.md '这是文件说明'")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    message_text = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if not file_path.exists():
        print(f"❌ 文件不存在：{file_path}")
        sys.exit(1)
    
    print("📤 Feishu 文件发送")
    print("=" * 60)
    print(f"文件：{file_path.name}")
    print(f"大小：{file_path.stat().st_size} bytes")
    print(f"接收者：{USER_OPEN_ID}")
    print("=" * 60)
    
    try:
        # 步骤 1: 获取 token
        print("\n1️⃣ 获取 access_token...")
        token = get_tenant_access_token()
        print(f"✅ Token 获取成功")
        
        # 步骤 2: 上传文件
        print("\n2️⃣ 上传文件到飞书...")
        file_key, file_url = upload_file(token, file_path)
        
        # 步骤 3: 发送消息
        print("\n3️⃣ 发送文件消息...")
        message_id = send_file_message(token, USER_OPEN_ID, file_key, file_path.name, file_url, message_text)
        
        print("\n" + "=" * 60)
        print("✅ 文件发送完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 发送失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
