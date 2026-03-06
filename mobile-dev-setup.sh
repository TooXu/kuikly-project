#!/bin/bash

# 移动端开发环境快速启动脚本
# 适用于 iOS、Android、鸿蒙和KMP跨端开发

echo "📱 移动端开发环境快速启动"
echo "========================"

# 设置环境变量
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17.0.18.0.8-1.0.2.1.al8.x86_64
export ANDROID_HOME=$HOME/android-sdk
export ANDROID_SDK_ROOT=$HOME/android-sdk
export PATH=$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH

# Flutter路径
export FLUTTER_HOME=$HOME/flutter
export PATH=$FLUTTER_HOME/bin:$PATH

# Gradle路径
export GRADLE_HOME=$HOME/gradle
export PATH=$GRADLE_HOME/bin:$PATH

echo "✅ 环境变量已设置"
echo "Java: $(java -version 2>&1 | head -1)"
echo "Android SDK: $ANDROID_HOME"
echo "Flutter: $FLUTTER_HOME"
echo "Gradle: $GRADLE_HOME"

# 创建项目目录
mkdir -p ~/mobile-projects

echo "📁 项目目录已创建: ~/mobile-projects"

# 验证工具
echo ""
echo "🔧 工具验证:"
echo "- Java: $(java -version 2>&1 | head -1)"
if command -v flutter &> /dev/null; then
    echo "- Flutter: $(flutter --version 2>&1 | head -1)"
else
    echo "- Flutter: 未完全安装"
fi
if command -v gradle &> /dev/null; then
    echo "- Gradle: $(gradle --version 2>&1 | head -1)"
else
    echo "- Gradle: 未完全安装"
fi
if command -v sdkmanager &> /dev/null; then
    echo "- Android SDK: 已配置"
else
    echo "- Android SDK: 需要完成安装"
fi

echo ""
echo "🚀 环境准备就绪！"
echo "使用以下命令创建新项目:"
echo "  - KMP项目: cp -r kmp-project-template ~/mobile-projects/my-kmp-app"
echo "  - Flutter项目: flutter create my_flutter_app"
echo "  - Android项目: 使用Android Studio或gradle init"