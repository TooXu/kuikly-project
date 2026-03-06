#!/bin/bash

# 移动端开发桌面环境启动脚本
echo "🚀 启动移动端开发桌面环境..."

# 设置环境变量
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17.0.18.0.8-1.0.2.1.al8.x86_64
export ANDROID_HOME=/home/admin/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 启动XFCE桌面环境
echo "🖥️  启动XFCE桌面环境..."
startxfce4 &

# 启动VS Code（可选）
echo "💻 启动VS Code..."
code --new-window &

echo "✅ 桌面环境启动完成！"
echo "📱 现在可以开始移动端开发了！"

# 显示环境信息
echo ""
echo "=== 环境信息 ==="
java -version
echo "Android SDK: $ANDROID_HOME"
echo "Flutter: $(which flutter)"
echo "Gradle: $(which gradle)"