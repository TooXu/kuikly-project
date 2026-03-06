# Kuikly 跨端框架配置

## 框架概述
Kuikly 是一个基于 Kotlin Multiplatform (KMP) 的跨端开发框架，支持 iOS、Android 和鸿蒙应用开发。

## 技术栈
- **核心语言**: Kotlin
- **跨平台**: Kotlin Multiplatform (KMP)
- **iOS**: Kotlin/Native + Swift/Objective-C 互操作
- **Android**: Kotlin/JVM
- **鸿蒙**: Kotlin + HarmonyOS SDK
- **共享代码**: 业务逻辑、数据模型、网络层

## 环境要求
- **JDK**: Java 17 (已安装)
- **Android SDK**: 已配置
- **Xcode**: iOS 开发需要 (macOS only)
- **HarmonyOS SDK**: 鸿蒙开发需要
- **Gradle**: 8.0+ (已安装)

## 项目结构
```
kuikly-project/
├── shared/                 # 共享代码模块
│   ├── src/
│   │   ├── commonMain/     # 通用 Kotlin 代码
│   │   ├── androidMain/    # Android 特定代码
│   │   ├── iosMain/        # iOS 特定代码
│   │   └── harmonyMain/    # 鸿蒙特定代码
├── androidApp/            # Android 应用
├── iosApp/                # iOS 应用  
├── harmonyApp/            # 鸿蒙应用
└── build.gradle.kts       # KMP 配置
```

## 开发工作流
1. **共享代码开发**: 在 `shared/commonMain` 中编写业务逻辑
2. **平台特定实现**: 在对应平台目录中实现平台特定功能
3. **构建和测试**: 使用 Gradle 构建各平台应用
4. **部署**: 分别部署到各应用商店

## 常用命令
```bash
# 构建所有平台
./gradlew build

# 运行 Android 应用
./gradlew :androidApp:installDebug

# 构建 iOS 框架 (macOS)
./gradlew :shared:compileKotlinIosX64

# 构建鸿蒙应用
./gradlew :harmonyApp:assemble
```

## 调试和测试
- **单元测试**: 在 `commonTest` 目录中编写
- **集成测试**: 各平台特定测试
- **调试工具**: Android Studio, Xcode, DevEco Studio