#!/bin/bash

# 移动端开发桌面环境快速启动脚本
echo "🚀 启动移动端开发桌面环境..."

# 设置环境变量
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17.0.18.0.8-1.0.2.1.al8.x86_64
export ANDROID_HOME=$HOME/android-sdk
export PATH=$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH
export FLUTTER_HOME=$HOME/flutter
export PATH=$FLUTTER_HOME/bin:$PATH
export GRADLE_HOME=$HOME/gradle-8.5
export PATH=$GRADLE_HOME/bin:$PATH

# 创建桌面快捷方式目录
mkdir -p $HOME/Desktop

# 创建VS Code快捷方式
if [ -f "/usr/bin/code" ]; then
    echo "Creating VS Code desktop shortcut..."
    cat > $HOME/Desktop/VSCode.desktop << EOF
[Desktop Entry]
Name=Visual Studio Code
Comment=Code Editing. Redefined.
Exec=/usr/bin/code --no-sandbox --user-data-dir
Icon=/usr/share/icons/hicolor/256x256/apps/vscode.png
Terminal=false
Type=Application
Categories=Development;IDE;
EOF
    chmod +x $HOME/Desktop/VSCode.desktop
fi

# 创建终端快捷方式
cat > $HOME/Desktop/Terminal.desktop << EOF
[Desktop Entry]
Name=Terminal
Comment=Terminal Emulator
Exec=xfce4-terminal
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=System;TerminalEmulator;
EOF
chmod +x $HOME/Desktop/Terminal.desktop

# 创建Android Studio快捷方式（如果安装）
cat > $HOME/Desktop/AndroidStudio.desktop << EOF
[Desktop Entry]
Name=Android Studio
Comment=Android Development IDE
Exec=bash -c 'cd \$HOME && ./android-studio/bin/studio.sh'
Icon=android-studio
Terminal=false
Type=Application
Categories=Development;IDE;
EOF
chmod +x $HOME/Desktop/AndroidStudio.desktop

# 配置XFCE面板
echo "Configuring XFCE panel for mobile development..."
xfconf-query -c xfce4-panel -p /panels/panel-1/autohide -s false
xfconf-query -c xfce4-panel -p /panels/panel-1/position -s p=6;x=0;y=0

echo "✅ 桌面环境配置完成！"
echo "💡 使用建议："
echo "   - 双击桌面图标启动开发工具"
echo "   - 使用终端进行命令行操作"
echo "   - 所有移动端开发工具已配置完成"