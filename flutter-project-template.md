# Flutter 项目模板配置

## 项目结构
```
flutter_app/
├── android/              # Android 平台代码
├── ios/                  # iOS 平台代码  
├── lib/                  # Dart 核心代码
│   ├── main.dart         # 应用入口
│   ├── models/           # 数据模型
│   ├── screens/          # 页面组件
│   ├── widgets/          # 自定义组件
│   └── utils/            # 工具类
├── test/                 # 单元测试
├── integration_test/     # 集成测试
├── pubspec.yaml          # 依赖配置
└── README.md             # 项目说明
```

## pubspec.yaml 配置示例
```yaml
name: flutter_app
description: "跨平台移动应用"
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  # 状态管理
  provider: ^6.0.0
  # 网络请求
  dio: ^5.0.0
  # JSON序列化
  json_serializable: ^6.0.0
  # 路由
  go_router: ^12.0.0
  # 国际化
  flutter_localizations:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0
  build_runner: ^2.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
    - assets/icons/
```

## 支持的平台
- ✅ Android (API 21+)
- ✅ iOS (11.0+)
- ✅ Web (可选)
- ✅ Desktop (可选)

## 开发工作流
1. **初始化项目**: `flutter create --org com.yourcompany flutter_app`
2. **添加依赖**: 在 `pubspec.yaml` 中添加所需包
3. **运行代码生成**: `flutter pub run build_runner build --delete-conflicting-outputs`
4. **开发调试**: `flutter run`
5. **构建发布**: 
   - Android: `flutter build apk --release`
   - iOS: `flutter build ios --release`

## 与KMP集成
可以通过以下方式集成Kotlin Multiplatform模块：
1. 在 `android/build.gradle` 中添加KMP模块依赖
2. 使用 platform channels 进行Dart和Kotlin代码通信
3. 共享业务逻辑和数据模型

## 性能优化建议
- 使用 const 构造函数减少重建
- 合理使用 ListView.builder 避免内存问题
- 图片资源使用适当的压缩格式
- 异步操作使用 FutureBuilder 或 StreamBuilder