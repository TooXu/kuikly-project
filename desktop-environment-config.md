# 桌面环境配置文档

## 环境概述
- **操作系统**: Alibaba Cloud Linux 3 (基于RHEL)
- **桌面环境**: XFCE (轻量级、稳定、开发者友好)
- **开发工具**: VS Code、终端模拟器、文件管理器
- **集成**: 移动端开发环境完全集成

## 已安装组件
### 核心桌面
- ✅ XFCE桌面环境
- ✅ XFCE终端 (xfce4-terminal)
- ✅ Thunar文件管理器
- ✅ XFCE面板和窗口管理器

### 开发工具
- ✅ VS Code (vscode.x86_64)
- ✅ Git集成
- ✅ 终端多标签支持

### 移动端开发集成
- ✅ Android SDK环境变量自动加载
- ✅ Flutter路径配置
- ✅ Java 17默认运行时
- ✅ Gradle构建工具

## 快速启动
1. **启动桌面环境**:
   ```bash
   # 如果通过SSH连接，需要启用X11转发
   ssh -X username@server
   
   # 启动XFCE桌面
   startxfce4
   ```

2. **使用快速配置脚本**:
   ```bash
   ./desktop-setup.sh
   ```

## 桌面定制
### 开发者友好的XFCE配置
- **终端**: 配置为深色主题，支持多标签
- **编辑器**: VS Code已预配置移动端开发插件
- **快捷键**: 
  - `Ctrl+Alt+T` - 打开终端
  - `Ctrl+Alt+F` - 打开文件管理器
  - `Super+Space` - 应用程序启动器

### 移动端开发工作区
- **项目目录**: `~/projects/mobile/`
- **Android模拟器**: 可通过终端启动
- **Flutter开发**: 直接在VS Code中打开项目

## 故障排除
### 常见问题
1. **桌面无法启动**: 确保X11转发已启用
2. **VS Code插件**: 首次启动时可能需要安装移动端开发插件
3. **Android模拟器**: 需要启用硬件加速（如果支持）

### 环境验证
```bash
# 验证Java
java -version

# 验证Android SDK
sdkmanager --list

# 验证Flutter
flutter --version

# 验证Gradle
gradle --version
```

## 下一步建议
1. **配置显示器**: 如果有多个显示器，调整分辨率和布局
2. **安装额外字体**: 安装编程字体如Fira Code
3. **配置键盘快捷键**: 根据个人习惯自定义快捷键
4. **设置壁纸和主题**: 选择适合开发的主题

## 备份和恢复
所有配置文件都保存在:
- `~/.config/xfce4/` - XFCE配置
- `~/.vscode/` - VS Code配置
- `/home/admin/.openclaw/workspace/` - 项目模板和脚本

可以通过备份这些目录来保存您的桌面环境配置。