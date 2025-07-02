#!/usr/bin/env python3
import json
import os
import sys
import subprocess
import platform
import shutil
import time
from pathlib import Path

def print_header():
    print("""
    ╔═══════════════════════════════════════════╗
    ║     CC-Notifier Interactive Setup         ║
    ║     Claude Code 通知助手安装向导          ║
    ╚═══════════════════════════════════════════╝
    """)

def print_progress(step, total, message):
    """显示进度条"""
    progress = int((step / total) * 40)
    bar = "█" * progress + "░" * (40 - progress)
    print(f"\r[{bar}] {step}/{total} - {message}", end="", flush=True)
    if step == total:
        print()  # 换行

def check_dependencies():
    """检查并安装依赖"""
    print("\n🔍 检查依赖...")
    
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("❌ 需要 Python 3.6 或更高版本")
        return False
    
    # 检查 pip
    pip_cmd = "pip3" if shutil.which("pip3") else "pip"
    if not shutil.which(pip_cmd):
        print("❌ 未找到 pip，请先安装 pip")
        return False
    
    # 检查 requests 库
    try:
        import requests
        print("✅ 依赖检查通过")
        return True
    except ImportError:
        print("📦 缺少 requests 库，正在安装...")
        try:
            subprocess.run([pip_cmd, "install", "requests"], check=True, capture_output=True)
            print("✅ requests 库安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ 安装 requests 库失败")
            print(f"   请手动运行: {pip_cmd} install requests")
            return False

def find_claude_settings_path():
    """查找 Claude Code settings.json 文件路径"""
    home = Path.home()
    possible_paths = [
        home / ".claude" / "settings.json",
        home / "Library" / "Application Support" / "Claude" / "settings.json",  # macOS
        home / "AppData" / "Roaming" / "Claude" / "settings.json",  # Windows
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # 默认路径
    return home / ".claude" / "settings.json"

def get_input_with_default(prompt, default=""):
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("❌ 此项为必填项，请输入有效值")

def validate_url(url):
    return url.startswith("http://") or url.startswith("https://")

def copy_to_clipboard(text):
    """将文本复制到剪贴板"""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
        elif system == "Linux":
            # 尝试多个剪贴板工具
            for cmd in [['xclip', '-selection', 'clipboard'], ['xsel', '--clipboard', '--input']]:
                try:
                    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
                except:
                    continue
            return False
        elif system == "Windows":
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            process.communicate(text.encode('utf-8'))
        else:
            return False
        return True
    except Exception as e:
        print(f"\n⚠️ 剪贴板操作失败: {e}")
        return False

def verify_setup(config):
    """验证安装配置"""
    print("\n🔍 验证配置...")
    issues = []
    
    # 检查通知服务配置
    if not config.get("feishu_webhook_url") and not config.get("ios_push_url"):
        issues.append("未配置任何通知服务（飞书或iOS推送）")
    
    # 检查脚本文件
    notifier_path = os.path.join(os.path.dirname(__file__), "cc_notifier.py")
    if not os.path.exists(notifier_path):
        issues.append("未找到 cc_notifier.py 文件")
    
    # 检查 Python 版本和依赖
    try:
        import requests
    except ImportError:
        issues.append("requests 库未安装")
    
    # 检查 Claude Code 配置目录
    settings_path = find_claude_settings_path()
    if not settings_path.parent.exists():
        issues.append(f"Claude Code 配置目录不存在: {settings_path.parent}")
    
    if issues:
        print("\n❌ 发现以下问题：")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        return False
    else:
        print("✅ 所有检查通过")
        return True

def main():
    print_header()
    
    # 检查依赖
    print_progress(1, 8, "检查系统依赖")
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请解决后重试")
        sys.exit(1)
    time.sleep(0.5)
    
    print_progress(2, 8, "配置消息推送服务")
    print("\n\n📋 步骤 1/4: 配置消息推送服务")
    print("-" * 40)
    
    # 获取飞书 Webhook URL
    print("\n1️⃣ 飞书机器人 Webhook URL")
    print("   如果你使用飞书，请输入机器人的 Webhook URL")
    print("   留空则跳过飞书配置")
    feishu_url = get_input_with_default("飞书 Webhook URL", "")
    
    if feishu_url and not validate_url(feishu_url):
        print("⚠️  警告: URL 格式可能不正确，请确保以 http:// 或 https:// 开头")
    
    # 获取 iOS Push URL
    print("\n2️⃣ iOS 推送配置 (Bark)")
    print("   支持以下格式：")
    print("   - 完整 URL: https://api.day.app/YOUR_KEY")
    print("   - 仅 KEY: YOUR_KEY")
    print("   留空则跳过 iOS 推送配置")
    ios_push_url = get_input_with_default("Bark Push URL 或 KEY", "")
    
    # 询问是否默认启用 iOS 推送
    ios_push_enabled = "false"
    if ios_push_url:
        enable_ios = get_input_with_default("是否启用 iOS 推送? (y/n)", "y")
        ios_push_enabled = "true" if enable_ios.lower() in ['y', 'yes', '是'] else "false"
    
    print_progress(3, 8, "生成配置文件")
    print("\n\n📋 步骤 2/4: 生成配置文件")
    print("-" * 40)
    
    # 创建配置
    config = {
        "feishu_webhook_url": feishu_url,
        "ios_push_url": ios_push_url,
        "ios_push_enabled": ios_push_enabled == "true"
    }
    
    # 询问配置文件保存位置
    print("\n配置文件可以保存在以下位置：")
    print("1. 全局配置: ~/.cc-notifier/config.json")
    print("2. 本地配置: ./config.json (当前目录)")
    print("3. 仅使用环境变量 (不创建配置文件)")
    
    choice = get_input_with_default("请选择 (1/2/3)", "1")
    
    if choice == "1":
        # 全局配置
        config_dir = os.path.expanduser("~/.cc-notifier")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.json")
    elif choice == "2":
        # 本地配置
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    else:
        # 仅环境变量
        config_path = None
    
    if config_path:
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"✅ 配置文件已保存到: {config_path}")
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            print("\n📝 备选方案：使用环境变量配置")
            print("\n请将以下内容添加到您的 shell 配置文件（如 ~/.bashrc 或 ~/.zshrc）：")
            print("```bash")
            if feishu_url:
                print(f"export FEISHU_WEBHOOK_URL=\"{feishu_url}\"")
            if ios_push_url:
                print(f"export IOS_PUSH_URL=\"{ios_push_url}\"")
                print(f"export IOS_PUSH_ENABLED={ios_push_enabled}")
            print("```")
            print("\n然后运行 source ~/.bashrc (或 source ~/.zshrc) 使配置生效")
    else:
        print("\n📝 使用环境变量配置")
        print("\n请将以下内容添加到您的 shell 配置文件（如 ~/.bashrc 或 ~/.zshrc）：")
        print("```bash")
        if feishu_url:
            print(f"export FEISHU_WEBHOOK_URL=\"{feishu_url}\"")
        if ios_push_url:
            print(f"export IOS_PUSH_URL=\"{ios_push_url}\"")
            print(f"export IOS_PUSH_ENABLED={ios_push_enabled}")
        print("```")
        print("\n然后运行 source ~/.bashrc (或 source ~/.zshrc) 使配置生效")
    
    print_progress(4, 8, "生成 hooks 配置")
    print("\n\n📋 步骤 3/4: 生成 Claude Code hooks 配置")
    print("-" * 40)
    
    # 获取脚本的绝对路径
    notifier_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "cc_notifier.py"))
    
    # 生成 hooks 配置
    hooks_config = {
        "hooks": {
            "Stop": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f"python3 {notifier_path}"
                        }
                    ]
                }
            ]
        }
    }
    
    hooks_json = json.dumps(hooks_config, indent=2)
    
    print("📝 已生成 hooks 配置：")
    print("-" * 40)
    print(hooks_json)
    print("-" * 40)
    
    # 尝试复制到剪贴板
    if copy_to_clipboard(hooks_json):
        print("\n✅ 配置已复制到剪贴板！")
    else:
        print("\n⚠️  无法自动复制到剪贴板，请手动复制上面的配置")
    
    print_progress(5, 8, "配置 Claude Code")
    print("\n\n📋 步骤 4/4: 配置 Claude Code")
    print("-" * 40)
    
    # 查找 settings.json 路径
    settings_path = find_claude_settings_path()
    print(f"\n🔍 Claude Code 配置文件位置: {settings_path}")
    
    # 询问是否自动打开文件
    if settings_path.parent.exists():
        auto_open = get_input_with_default("\n是否自动打开 settings.json 文件? (y/n)", "y")
        if auto_open.lower() in ['y', 'yes', '是']:
            try:
                # 确保目录存在
                settings_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 如果文件不存在，创建基础结构
                if not settings_path.exists():
                    with open(settings_path, 'w') as f:
                        json.dump({"hooks": {}}, f, indent=2)
                
                # 尝试打开文件
                if platform.system() == "Darwin":
                    subprocess.run(["open", str(settings_path)])
                elif platform.system() == "Windows":
                    subprocess.run(["notepad", str(settings_path)])
                else:
                    # Linux - 尝试常见编辑器
                    for editor in ["xdg-open", "gnome-open", "kde-open", "nano", "vi"]:
                        if shutil.which(editor):
                            subprocess.run([editor, str(settings_path)])
                            break
                print("\n✅ 已打开 settings.json 文件")
            except Exception as e:
                print(f"\n⚠️ 无法自动打开文件: {e}")
    
    print("\n请按照以下步骤完成配置：")
    print(f"\n1. 确保 settings.json 文件位于: {settings_path}")
    print("\n2. 找到 \"hooks\" 字段（如果没有则添加）")
    print("\n3. 将剪贴板中的内容粘贴到 \"hooks\" 字段中")
    print("\n4. 保存文件并重启 Claude Code")
    
    print("\n📌 示例 settings.json 结构：")
    print("-" * 40)
    example_settings = {
        "theme": "auto",
        "hooks": hooks_config,
        "other_settings": "..."
    }
    print(json.dumps(example_settings, indent=2)[:200] + "...")
    
    print_progress(6, 8, "验证安装")
    
    # 添加测试通知功能
    print("\n\n📋 步骤 5/5: 测试通知")
    print("-" * 40)
    test_notify = get_input_with_default("\n是否发送测试通知? (y/n)", "y")
    
    if test_notify.lower() in ['y', 'yes', '是']:
        print_progress(7, 8, "发送测试通知")
        try:
            # 创建测试数据
            test_data = {
                "event_type": "Stop",
                "session_id": "test-session-123",
                "stop_hook_active": False,
                "transcript_path": ""
            }
            
            # 调用 cc_notifier.py 进行测试
            notifier_path = os.path.join(os.path.dirname(__file__), "cc_notifier.py")
            process = subprocess.Popen(
                ["python3", notifier_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(json.dumps(test_data).encode())
            
            if process.returncode == 0:
                print("\n✅ 测试通知发送成功！")
                print("   请检查您的飞书和手机是否收到通知")
            else:
                print("\n❌ 测试通知发送失败")
                if stderr:
                    print(f"   错误信息: {stderr.decode()}")
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
    
    print_progress(8, 8, "完成！")
    
    # 最终验证
    if verify_setup(config):
        print("\n\n✨ 安装完成！")
        print("\n📌 后续步骤：")
        print("1. 确保已将 hooks 配置添加到 settings.json")
        print("2. 重启 Claude Code 使配置生效")
        print("3. 执行任意命令测试通知功能")
        
        print("\n💡 提示：")
        print("- 可以通过环境变量临时覆盖配置：")
        print("  export IOS_PUSH_URL=your_new_url")
        print("  export IOS_PUSH_ENABLED=true")
        print("\n- 查看日志排查问题：")
        print("  tail -f ~/.claude/logs/claude.log")
        
        print("\n🎉 祝您使用愉快！")
    else:
        print("\n⚠️ 安装完成但存在一些问题，请检查并修复")
        print("\n可能的解决方案：")
        print("1. 确保至少配置了一个通知服务（飞书或iOS）")
        print("2. 检查 cc_notifier.py 是否在同一目录")
        print("3. 运行 pip3 install requests 安装依赖")
        print("4. 确保 Claude Code 已安装并运行过至少一次")

if __name__ == "__main__":
    main()