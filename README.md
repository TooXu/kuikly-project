# kuikly-project

基于 KuiklyUI 框架开发的 Apple Intelligence 风格交互页面。

## 功能特性

- **IM 聊天框对话页面**：类似消息应用的聊天界面
- **Apple Intelligence 交互效果**：点击 AI 按钮时，屏幕四周出现彩色光晕
- **呼吸动画效果**：光晕具有平滑的呼吸动画，颜色在多种色调间渐变
- **基于 KuiklyUI**：使用 KuiklyUI 的 Compose DSL 和动画系统

## 技术实现

- 使用 KuiklyUI Compose DSL 构建 UI
- 利用 KuiklyUI 的动画系统实现呼吸效果
- 采用线性渐变模拟径向光晕效果（KuiklyUI 目前不支持径向渐变）
- 响应式布局适配不同屏幕尺寸

## 项目结构

```
src/
└── commonMain/
    └── kotlin/com/tooxu/kuiklyproject/
        └── AppleIntelligenceChatPage.kt  # 主要页面组件
```

## 运行指南

由于这是 KuiklyUI 项目，需要集成到 KuiklyUI 的 demo 环境中运行：

1. **克隆 KuiklyUI 项目**
   ```bash
   git clone https://github.com/Tencent-TDS/KuiklyUI.git
   ```

2. **复制代码到 KuiklyUI demo**
   ```bash
   cp src/commonMain/kotlin/com/tooxu/kuiklyproject/AppleIntelligenceChatPage.kt KuiklyUI/demo/src/commonMain/kotlin/com/tencent/kuikly/demo/pages/
   ```

3. **注册页面路由**
   - 编辑 `KuiklyUI/demo/src/commonMain/kotlin/com/tencent/kuikly/demo/app/AppRouter.kt`
   - 在 pages 列表中添加 `AppleIntelligenceChatPage::class`

4. **配置开发环境**
   - Android Studio (JDK 17)
   - Xcode + CocoaPods (iOS)
   - DevEco Studio (鸿蒙)

5. **运行对应平台的示例应用**

## 依赖

- KuiklyUI Framework
- Kotlin Multiplatform
- KuiklyUI Compose (Jetpack Compose 修改版)