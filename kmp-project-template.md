# Kotlin Multiplatform (KMP) 项目模板

## 项目结构
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
│           └── res/
└── iosApp/
    └── (Xcode project)
```

## 核心配置文件

### build.gradle.kts (项目根目录)
```kotlin
plugins {
    kotlin("multiplatform") version "1.9.20"
    id("com.android.application") version "8.2.0" apply false
}

repositories {
    mavenCentral()
    google()
}
```

### settings.gradle.kts
```kotlin
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "MyKMPApp"
include(":androidApp")
include(":shared")
```

### shared/build.gradle.kts
```kotlin
import org.jetbrains.kotlin.gradle.plugin.mpp.KotlinNativeTarget

plugins {
    kotlin("multiplatform")
    id("com.android.library")
    id("org.jetbrains.compose")
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions {
                jvmTarget = "17"
            }
        }
    }
    
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "shared"
        }
    }
    
    // 鸿蒙支持 (需要额外配置)
    // harmony()
    
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation(compose.runtime)
                implementation(compose.foundation)
                implementation(compose.material)
                implementation(compose.ui)
                implementation(compose.components.resources)
            }
        }
        
        val androidMain by getting {
            dependencies {
                api("androidx.activity:activity-compose:1.8.0")
                api("androidx.appcompat:appcompat:1.6.1")
                api("androidx.core:core-ktx:1.12.0")
            }
        }
        
        val iosMain by getting
        
        // val harmonyMain by getting
    }
}

android {
    namespace = "com.example.mykmpapp"
    compileSdk = 34
    defaultConfig {
        minSdk = 21
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
```

## Kuikly框架集成

### Kuikly特定配置
- 使用Kuikly的UI组件库
- 集成跨平台状态管理
- 支持鸿蒙特有的API调用

### 鸿蒙支持配置
```kotlin
// 在shared/src/harmonyMain/kotlin/中添加鸿蒙特定实现
expect class PlatformLogger() {
    fun log(message: String)
}

actual class PlatformLogger {
    actual fun log(message: String) {
        // 鸿蒙日志实现
        ohos.hiviewdfx.HiLog.info(LOG_LABEL, message)
    }
}
```

## 构建命令

### Android构建
```bash
./gradlew :androidApp:assembleDebug
```

### iOS构建
```bash
./gradlew :shared:packForXcode
# 然后在Xcode中构建
```

### 鸿蒙构建
```bash
# 需要DevEco Studio或命令行工具
./gradlew :harmonyApp:assembleHap
```

## 开发工作流

1. **共享代码开发** - 在`shared/src/commonMain`中编写业务逻辑
2. **平台特定实现** - 在对应平台的source set中实现平台特定功能
3. **UI开发** - 使用Compose Multiplatform或平台原生UI
4. **测试** - 编写跨平台测试和平台特定测试
5. **构建和部署** - 使用Gradle构建各平台应用

## 调试和测试

### 单元测试
- `commonTest` - 跨平台测试
- `androidTest` - Android特定测试
- `iosTest` - iOS特定测试

### 集成测试
- 使用Ktor或OkHttp进行网络测试
- 使用SQLDelight进行数据库测试
- 使用MockK进行模拟测试

## 性能优化

- 使用Kotlin/Native内存管理最佳实践
- 避免不必要的跨平台调用
- 使用协程进行异步操作
- 优化资源加载和缓存策略