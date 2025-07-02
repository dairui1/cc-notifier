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
1. ✅ 检查系统依赖（Python 3.6+，自动安装 requests）
2. 📝 配置飞书和/或 iOS 推送服务
3. 🗂️  选择配置文件保存位置（全局/本地/环境变量）
4. 🔧 生成 Claude Code hooks 配置（仅 Stop hook）
5. 📋 自动复制 hooks 配置到剪贴板
6. 📂 可选自动打开 settings.json 文件
7. 🧪 发送测试通知验证配置
8. 🔍 验证所有配置是否正确

## 🛠️ 手动配置 Manual Setup

如果自动安装失败或需要手动配置：
If automatic setup fails or you need to configure manually:

### 1. 检查系统要求和依赖 Check system requirements and dependencies
```bash
# 检查 Python 版本（需要 3.6+）
python3 --version

# 安装依赖
pip3 install requests
```

### 2. 配置通知服务 Configure notification services

#### 选项A：使用配置文件 Option A: Using config file

**全局配置（推荐）Global config (Recommended):**
```bash
# 创建全局配置目录
mkdir -p ~/.cc-notifier

# 创建配置文件
cat > ~/.cc-notifier/config.json << 'EOF'
{
  "feishu_webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_KEY",
  "ios_push_url": "https://api.day.app/YOUR_BARK_KEY",
  "ios_push_enabled": true
}
EOF

# 编辑配置文件，填写你的实际 URL
nano ~/.cc-notifier/config.json
```

**本地配置 Local config:**
```bash
# 复制示例配置
cp config.example.json config.json

# 编辑配置文件
nano config.json
```

#### 选项B：使用环境变量 Option B: Using environment variables
```bash
# 添加到你的 shell 配置文件 (~/.bashrc 或 ~/.zshrc)
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_KEY"
export IOS_PUSH_URL="https://api.day.app/YOUR_BARK_KEY"  # 或者仅填写 KEY
export IOS_PUSH_ENABLED="true"

# 使配置生效
source ~/.bashrc  # 或 source ~/.zshrc
```

### 3. 配置 Claude Code hooks Configure Claude Code hooks

#### 3.1 找到 Claude Code 配置文件位置
Claude Code 配置文件通常位于：
- **macOS**: `~/.claude/settings.json`
- **Linux**: `~/.claude/settings.json`
- **Windows**: `%USERPROFILE%\.claude\settings.json`

#### 3.2 添加 hooks 配置
在你的 `~/.claude/settings.json` 中添加（**注意：只需要 Stop hook**）：
Add to your `~/.claude/settings.json` (**Note: Only Stop hook is needed**):
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /绝对路径/到/cc_notifier.py"
          }
        ]
      }
    ]
  }
}
```

**获取脚本绝对路径：**
```bash
# 在项目目录中运行
pwd
# 输出类似：/Users/username/cc-notifier
# 则完整路径为：/Users/username/cc-notifier/cc_notifier.py
```

#### 3.3 完整配置示例
如果你的 `settings.json` 已有其他配置，请合并：
```json
{
  "theme": "auto",
  "fontSize": 14,
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /Users/username/cc-notifier/cc_notifier.py"
          }
        ]
      }
    ]
  }
}
```

### 4. 测试配置 Test configuration
```bash
# 手动测试通知脚本
echo '{"event_type":"Stop","session_id":"test-123","stop_hook_active":false,"transcript_path":""}' | python3 cc_notifier.py

# 检查是否收到测试通知
```

## ⚙️ 配置优先级 Configuration Priority

配置加载优先级（从高到低）：
1. 环境变量 (Environment variables)
2. 配置文件 (`~/.cc-notifier/config.json` 或 `./config.json`)
3. 默认值 (Default values)

## 📱 支持的事件 Supported Events

- **Stop**: 任务完成时触发，显示 Claude 的最后回复（主要事件）
- **Notification**: 通用通知事件（iOS 推送暂时关闭以减少打扰）

> 💡 **注意**：自动安装只配置 Stop 事件以避免过多通知。如需其他事件，请手动添加到 hooks 配置中。

## 🔧 故障排除 Troubleshooting

### 通知未收到 Notification not received
1. **检查配置**：
   ```bash
   # 检查配置文件是否存在
   ls -la ~/.cc-notifier/config.json
   # 或
   ls -la ./config.json
   
   # 检查环境变量
   echo $FEISHU_WEBHOOK_URL
   echo $IOS_PUSH_URL
   echo $IOS_PUSH_ENABLED
   ```

2. **验证 URL 格式**：
   - 飞书 Webhook: 必须以 `https://open.feishu.cn/` 开头
   - iOS Push: 支持完整 URL 或仅 KEY 格式

3. **测试通知功能**：
   ```bash
   # 手动测试
   echo '{"event_type":"Stop","session_id":"test-123","stop_hook_active":false,"transcript_path":""}' | python3 cc_notifier.py
   ```

4. **查看详细日志**：
   ```bash
   # Claude Code 日志
   tail -f ~/.claude/logs/claude.log
   
   # 如果使用 systemd 或其他日志系统
   journalctl -f | grep claude
   ```

### 依赖问题 Dependency issues
```bash
# 检查 Python 版本（需要 3.6+）
python3 --version

# 安装/重新安装依赖
pip3 install requests

# 如果使用虚拟环境
pip3 install -r requirements.txt
```

### hooks 配置问题 Hooks configuration issues
1. **检查 settings.json 语法**：
   ```bash
   # 验证 JSON 格式
   python3 -m json.tool ~/.claude/settings.json
   ```

2. **确认脚本路径**：
   ```bash
   # 获取绝对路径
   realpath cc_notifier.py
   
   # 测试脚本是否可执行
   python3 /path/to/cc_notifier.py --help 2>/dev/null || echo "脚本路径可能不正确"
   ```

3. **重启 Claude Code** 使配置生效

### 权限问题 Permission issues
```bash
# 确保脚本有执行权限
chmod +x cc_notifier.py setup.py

# 检查文件权限
ls -la cc_notifier.py
```

### 配置验证 Configuration validation
运行自动验证脚本：
```bash
python3 -c "
import sys
sys.path.append('.')
from setup import verify_setup
config = {'feishu_webhook_url': '', 'ios_push_url': ''}
verify_setup(config)
"
```

## 📄 许可证 License

MIT License