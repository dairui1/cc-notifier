# CC-Notifier

Claude Code 通知助手 - 接收 Claude Code 事件并发送到飞书和 iOS 推送通知。

Claude Code notification webhook handler for Feishu (Lark) and iOS push notifications.

## ✨ 功能特性 Features

- 🔔 支持飞书机器人 Webhook 通知 (Feishu webhook notifications)
- 📱 支持 iOS Bark 推送通知 (iOS push notifications via Bark)
- 🚀 一键安装脚本，自动配置 (One-click setup with auto-configuration)
- 🔧 支持环境变量覆盖配置 (Environment variable overrides)
- ✅ 任务完成时自动通知 (Auto-notify on task completion)
- 📊 安装进度实时显示 (Real-time installation progress)
- 🔍 自动配置验证 (Automatic configuration validation)

## 🚀 快速开始 Quick Start

### 自动安装（推荐）Automatic Setup (Recommended)

运行交互式安装向导：
```bash
python3 setup.py
```

安装向导将自动完成：
1. ✅ 检查并安装依赖（自动安装 requests）
2. 📝 配置飞书和/或 iOS 推送服务
3. 🔧 生成 Claude Code hooks 配置
4. 📋 自动复制配置到剪贴板
5. 📂 可选自动打开 settings.json 文件
6. 🧪 发送测试通知验证配置
7. 🔍 验证所有配置是否正确

## 🛠️ 手动配置 Manual Setup

如果自动安装失败或需要手动配置：
If automatic setup fails or you need to configure manually:

### 1. 安装依赖 Install dependencies
```bash
pip install -r requirements.txt
```

### 2. 配置通知服务 Configure notification services

#### 选项A：使用配置文件 Option A: Using config file
复制示例配置并编辑：
Copy the example config and edit it:
```bash
cp config.example.json config.json
# 编辑 config.json，填写你的 URL
# Edit config.json with your URLs
```

或者创建全局配置：
Or create a global config:
```bash
mkdir -p ~/.cc-notifier
cp config.example.json ~/.cc-notifier/config.json
# 编辑 ~/.cc-notifier/config.json
# Edit ~/.cc-notifier/config.json
```

#### 选项B：使用环境变量 Option B: Using environment variables
```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_KEY"
export IOS_PUSH_URL="https://api.day.app/YOUR_BARK_KEY"
export IOS_PUSH_ENABLED="true"
```

### 3. 配置 Claude Code hooks Configure Claude Code hooks

在你的 `~/.claude/settings.json` 中添加：
Add to your `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "python3 /path/to/cc_notifier.py",
        "timeout": 10000,
        "stream_stdout": false
      }
    ],
    "PostToolUse": [
      {
        "command": "python3 /path/to/cc_notifier.py", 
        "timeout": 10000,
        "stream_stdout": false
      }
    ],
    "SessionStart": [
      {
        "command": "python3 /path/to/cc_notifier.py",
        "timeout": 10000,
        "stream_stdout": false
      }
    ],
    "Stop": [
      {
        "command": "python3 /path/to/cc_notifier.py",
        "timeout": 10000,
        "stream_stdout": false
      }
    ]
  }
}
```

## ⚙️ 配置优先级 Configuration Priority

配置加载优先级（从高到低）：
1. 环境变量 (Environment variables)
2. 配置文件 (`~/.cc-notifier/config.json` 或 `./config.json`)
3. 默认值 (Default values)

## 📱 支持的事件 Supported Events

- **Stop**: 任务完成时触发，显示 Claude 的最后回复
- **Notification**: 通用通知事件（iOS 推送暂时关闭以减少打扰）
- **ToolUse**: 工具使用事件（可选）
- **SessionStart**: 会话开始事件（可选）

## 🔧 故障排除 Troubleshooting

### 通知未收到 Notification not received
1. 检查配置文件或环境变量是否正确
   Check if the config file or environment variables are correct
2. 确保飞书 Webhook URL 有效
   Make sure the Feishu Webhook URL is valid
3. 确保 Bark 服务正常运行
   Make sure the Bark service is running properly
4. 查看 Claude Code 日志：
   Check Claude Code logs:
   ```bash
   tail -f ~/.claude/logs/claude.log
   ```

### 依赖问题 Dependency issues
```bash
pip3 install -r requirements.txt
```

### 权限问题 Permission issues
```bash
chmod +x cc_notifier.py setup.py
```

## 📄 许可证 License

MIT License