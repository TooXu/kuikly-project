#!/usr/bin/env node
const WebSocket = require('ws');
const crypto = require('crypto');

const GATEWAY_URL = 'ws://localhost:14961';
const TOKEN = '40c1dc3987f500cf2a80283d3f6ba725';

const cronJob = {
  name: "每日对话总结",
  schedule: { kind: "cron", expr: "0 19 * * *", tz: "Asia/Shanghai" },
  payload: { kind: "agentTurn", message: "请总结今天的所有对话内容，包括用户发送的消息和你的回复，并通过 Feishu 发送给用户。" },
  delivery: { mode: "announce", channel: "feishu" },
  sessionTarget: "isolated",
  enabled: true
};

const ws = new WebSocket(GATEWAY_URL);
let connected = false;

ws.on('open', () => {
  console.log('已连接到 Gateway');
});

ws.on('message', (data) => {
  const msg = JSON.parse(data.toString());
  console.log('收到消息:', JSON.stringify(msg, null, 2));
  
  // 处理连接挑战
  if (msg.type === 'event' && msg.event === 'connect.challenge') {
    const { nonce, ts } = msg.payload;
    const sig = crypto.createHmac('sha256', TOKEN).update(`${nonce}:${ts}`).digest('hex');
    console.log('发送连接响应...');
    ws.send(JSON.stringify({
      type: 'event',
      event: 'connect.response',
      payload: { nonce, sig }
    }));
  }
  // 认证成功
  else if (msg.type === 'event' && msg.event === 'connect.accepted') {
    console.log('✅ 连接已接受！');
    connected = true;
    console.log('添加定时任务...');
    ws.send(JSON.stringify({
      method: 'cron.add',
      params: { job: cronJob },
      id: 'add_cron_1'
    }));
  }
  // cron.add 结果
  else if (msg.id === 'add_cron_1') {
    if (msg.error) {
      console.error('❌ 添加失败:', JSON.stringify(msg.error));
    } else {
      console.log('✅ 定时任务添加成功！');
      console.log('任务 ID:', msg.result?.jobId);
    }
    ws.close();
  }
  // 其他错误
  else if (msg.error) {
    console.error('错误:', JSON.stringify(msg.error));
  }
});

ws.on('error', (err) => {
  console.error('连接错误:', err.message);
  process.exit(1);
});

ws.on('close', (code, reason) => {
  console.log(`连接已关闭 (code=${code})`);
  if (reason) console.log('原因:', reason.toString());
});

setTimeout(() => {
  if (!connected) {
    console.log('⚠️ 超时：未能建立连接');
  }
  ws.close();
  process.exit(connected ? 0 : 1);
}, 15000);
