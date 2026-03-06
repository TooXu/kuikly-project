# Mobile Development Skill

This skill provides comprehensive mobile development capabilities for iOS, Android, and HarmonyOS platforms, with special focus on Kotlin Multiplatform (KMP) and the Kuikly cross-platform framework.

## Capabilities

- **Android Development**: Full Android SDK setup with build tools, platform tools, and emulator support
- **iOS Development**: Xcode command line tools and iOS simulator management  
- **HarmonyOS Development**: DevEco Studio CLI and HarmonyOS SDK integration
- **Kotlin Multiplatform (KMP)**: Shared codebase development across all platforms
- **Kuikly Framework**: Custom cross-platform framework based on KMP architecture
- **Flutter Integration**: Optional Flutter support for additional cross-platform capabilities

## Environment Setup

### Java Requirements
- Java 17 (required for modern Android SDK)
- Java 11 (fallback for legacy projects)

### Android SDK Components
- Platform-tools (latest)
- Build-tools (34.0.0+ recommended)
- Platforms (android-34, android-35 for latest development)
- NDK (25.1.8937393+ for native development)

### iOS Requirements
- Xcode 15+ (macOS only)
- CocoaPods for dependency management

### HarmonyOS Requirements
- DevEco Studio 4.0+
- HarmonyOS SDK API Level 10+

### KMP Configuration
- Gradle 8.0+
- Kotlin 1.9.0+
- Multiplatform plugin configuration

## Usage Examples

### Create New KMP Project
```bash
./gradlew createKmpProject --name="MyApp" --targets="android,ios,harmonyos"
```

### Build for Specific Platform
```bash
# Android
./gradlew :androidApp:assembleDebug

# iOS  
./gradlew :iosApp:build

# HarmonyOS
./gradlew :harmonyosApp:assembleHap
```

### Kuikly Framework Commands
```bash
# Initialize Kuikly project
kuikly init --template=mobile-app

# Generate platform-specific code
kuikly generate --platform=android
kuikly generate --platform=ios  
kuikly generate --platform=harmonyos

# Build and deploy
kuikly build --target=all
kuikly deploy --platform=android --device=emulator
```

## Best Practices

1. **Shared Code Structure**: Keep business logic in shared modules, platform-specific code in respective targets
2. **Testing Strategy**: Implement unit tests in shared code, integration tests per platform
3. **Performance Monitoring**: Use platform-specific profiling tools (Android Profiler, Xcode Instruments, DevEco Performance Monitor)
4. **CI/CD Integration**: Configure workflows for automated testing and deployment across all platforms

## Troubleshooting

- **Android Build Issues**: Ensure JAVA_HOME points to Java 17, verify SDK paths
- **iOS Compilation**: Check Xcode command line tools installation, ensure proper signing certificates
- **HarmonyOS Emulator**: Verify DevEco Studio installation and emulator configuration
- **KMP Sync Issues**: Clean Gradle cache (`./gradlew clean`) and rebuild dependencies

## Dependencies

This skill requires the following system packages:
- `java-17-openjdk-devel`
- `android-sdk` (configured via cmdline-tools)
- `gradle` (8.0+)
- `nodejs` (for web components if needed)
- Platform-specific IDEs (Android Studio, Xcode, DevEco Studio)