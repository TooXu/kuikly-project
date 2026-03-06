# 移动端研发环境配置

## 环境要求
- **iOS开发**: 需要macOS系统（当前环境为Linux，无法进行iOS真机开发）
- **Android开发**: 已配置Java 17 + Android SDK
- **鸿蒙开发**: 需要HarmonyOS SDK（待安装）
- **KMP (Kotlin Multiplatform)**: 已配置Kotlin + Gradle

## 已安装组件
### Java
- Java 17 (OpenJDK 17.0.18)
- Java 11 (OpenJDK 11.0.25)

### Android SDK
- Platform-tools: 36.0.2
- Build-tools: 最新版本
- Platforms: Android 30-36
- Command-line tools: 20.0

### Flutter
- 版本: stable channel
- 位置: ~/flutter

### 构建工具
- Gradle: 8.5+
- Node.js: v24.13.0
- npm: 11.6.2
- pnpm: 已安装

## 待完成事项
1. **鸿蒙开发环境**: 需要安装HarmonyOS SDK和DevEco Studio
2. **iOS模拟器**: 无法在Linux上运行，需要macOS
3. **设备调试**: 配置ADB调试权限
4. **Kuikly框架**: 需要克隆和配置基于KMP的Kuikly跨端框架

## 环境变量配置
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17.0.18.0.8-1.0.2.1.al8.x86_64
export ANDROID_HOME=$HOME/android-sdk
export ANDROID_SDK_ROOT=$HOME/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
export FLUTTER_HOME=$HOME/flutter
export PATH=$PATH:$FLUTTER_HOME/bin
```

## 验证命令
- `java -version` - 验证Java 17
- `sdkmanager --list` - 验证Android SDK
- `flutter doctor` - 验证Flutter环境
- `gradle --version` - 验证Gradle