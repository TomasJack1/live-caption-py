# 🎧 实时字幕翻译工具 📝

![实时字幕翻译](https://img.shields.io/badge/实时-字幕翻译-brightgreen?style=flat-square) 
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&style=flat-square)
![PySide6](https://img.shields.io/badge/PySide6-6.4+-blue?logo=qt&style=flat-square)

**让你的视频会议、在线课程和媒体播放体验更加无障碍！**  
这个项目是一个基于Python的**实时字幕工具**，能够捕获系统音频生成的字幕并进行**实时翻译显示**！

## ✨ 核心功能

- **🎤 实时字幕捕获**：通过Windows Live Captions获取系统音频生成的字幕
- **🌍 多语言翻译**：将捕获的字幕实时翻译为目标语言
- **🪟 悬浮窗口**：半透明可拖拽的悬浮字幕窗口
- **📌 系统托盘支持**：最小化到系统托盘操作
- **👁️ 窗口管理**：一键切换Live Captions窗口的显示/隐藏

## 🚀 快速开始

### 1️⃣ 运行
  - 确保系统中已安装并启用Live Captions功能
  - 确保已经部署[bergamot-translation-server](https://github.com/TomasJack1/bergamot-translation-server)
### 3️⃣ 启动应用
从[Release](https://github.com/TomasJack1/live-caption-py/releases)下载应用

在`C:\Users\{这里是你的用户名}\AppData\Roaming\jiek`目录下的`livecaption.ini`配置文件中  如果没有则创建目录和文件 按如下格式配置

```ini
[General]
server_ip=localhost
server_port=8080


```

## 📁 项目结构

```
实时字幕翻译工具/
├── 📄 main.py                # 主程序入口
├── 📄 subtitle_ui.ui         # 字幕界面UI定义
├── 📄 translator.py          # 翻译服务客户端
├── 🖼️ app-icon.png           # 应用图标
├── 🔧 ruff.toml              # python ruff格式化工具配置
├── 📄 subtitle.qrc           # pyside6 资源文件定义
└── 📖 README.md              # 项目说明文档
```

## 📜 许可证

本项目采用[MIT许可证](LICENSE)。详情请参阅项目中的LICENSE文件。

---

**🎉 让语言不再成为障碍，享受无障碍的音频体验！**  
**🌟 欢迎贡献代码和提出改进建议！**