# 移动端开发项目模板

## 1. Kotlin Multiplatform (KMP) 项目结构

```
my-kmp-app/
├── build.gradle.kts
├── gradle.properties
├── settings.gradle.kts
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── shared/
│   ├── build.gradle.kts
│   └── src/
│       ├── commonMain/
│       │   ├── kotlin/
│       │   └── resources/
│       ├── androidMain/
│       │   ├── kotlin/
│       │   └── resources/
│       ├── iosMain/
│       │   ├── kotlin/
│       │   └── resources/
│       └── harmonyMain/
│           ├── kotlin/
│           └── resources/
├── androidApp/
│   ├── build.gradle.kts
│   └── src/
│       └── main/
│           ├── java/
│           ├── kotlin/
│           ├── res/
│           └── AndroidManifest.xml
├── iosApp/
│   └── (Xcode project)
└── harmonyApp/
    └── (Harmony project)
```

## 2. Kuikly框架配置

### build.gradle.kts (根目录)
```kotlin
plugins {
    kotlin("multiplatform") version "1.9.20"
    id("com.android.application") version "8.2.0" apply false
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions {
                jvmTarget = "17"
            }
        }
    }
    
    iosX64()
    iosArm64()
    iosSimulatorArm64()
    
    // 鸿蒙支持
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("io.ktor:ktor-client-core:2.3.5")
            }
        }
        
        val androidMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-okhttp:2.3.5")
            }
        }
        
        val iosMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-darwin:2.3.5")
            }
        }
    }
}
```

## 3. Flutter项目集成

如果需要在KMP项目中集成Flutter，可以使用以下结构：

```
my-hybrid-app/
├── flutter_module/          # Flutter模块
├── kmp_shared/             # KMP共享代码
├── android_app/            # Android原生应用
├── ios_app/               # iOS原生应用
└── harmony_app/           # 鸿蒙原生应用
```

## 4. 环境验证命令

### 验证Android环境
```bash
# 检查Android SDK
sdkmanager --list | grep "platforms;android"

# 检查构建工具
sdkmanager --list | grep "build-tools"
```

### 验证Flutter环境
```bash
# 检查Flutter安装
flutter --version

# 检查开发环境
flutter doctor
```

### 验证Gradle环境
```bash
# 检查Gradle版本
gradle --version
```

## 5. 开发工作流

### 创建新项目
```bash
# KMP项目
mkdir my-kmp-app && cd my-kmp-app
gradle init

# Flutter项目
flutter create my_flutter_app
```

### 构建和运行
```bash
# Android (KMP)
./gradlew :androidApp:assembleDebug

# iOS (KMP) - 需要在macOS上
./gradlew :iosApp:build

# Flutter
flutter run
```

## 6. 调试和测试

### 单元测试
- **commonTest**: 跨平台共享测试
- **androidTest**: Android特定测试  
- **iosTest**: iOS特定测试
- **harmonyTest**: 鸿蒙特定测试

### 集成测试
- 使用Ktor Client进行网络测试
- 使用SQLDelight进行数据库测试
- 使用Compose Multiplatform进行UI测试

## 7. 发布配置

### Android发布
- 配置签名密钥
- 设置ProGuard/R8混淆
- 生成AAB/APK

### iOS发布
- 配置Apple Developer证书
- 设置App Store Connect
- 生成IPA

### 鸿蒙发布
- 配置HMS Core
- 设置AppGallery Connect
- 生成HAP

## 8. CI/CD 配置建议

### GitHub Actions
- Android构建和测试
- iOS构建（需要macOS runner）
- Flutter测试
- 代码质量检查

### 自动化脚本
- 版本管理脚本
- 发布脚本
- 测试覆盖率报告