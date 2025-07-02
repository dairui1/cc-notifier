# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CC-Notifier is a notification webhook handler for Claude Code that sends events to Feishu (Lark) and iOS push notifications via Bark. The project is designed to be a simple, single-file Python script that processes Claude Code hook events.

## Key Architecture

### Core Components

1. **cc_notifier.py** - Main notification handler
   - Reads hook data from stdin
   - Extracts Claude's last message from JSONL transcript files
   - Formats messages using Feishu Card 2.0 format
   - Sends notifications to Feishu webhook and/or iOS Bark

2. **Event Handling**
   - Currently handles two events: `Stop` and `Notification`
   - Other events (ToolUse, SessionStart) are ignored
   - Stop events extract the last Claude message from transcript JSONL files

3. **Configuration System**
   - Priority: Environment variables > Config file > Defaults
   - Config locations: `~/.cc-notifier/config.json` or `./config.json`
   - Environment variables: `FEISHU_WEBHOOK_URL`, `IOS_PUSH_URL`, `IOS_PUSH_ENABLED`

## Common Tasks

### Running the Notifier
```bash
# Manual test (requires JSON input via stdin)
echo '{"event_type": "Stop", "transcript_path": "path/to/transcript.jsonl"}' | python3 cc_notifier.py
```

### Configuration
```bash
# Interactive setup
python3 setup.py

# Install dependencies
pip install -r requirements.txt
```

## Important Implementation Details

### JSONL Parsing
The `extract_last_message_from_jsonl()` function extracts the last `message.content[].text` from Claude's transcript files. This is the core functionality that displays Claude's actual responses in notifications.

### Feishu Card 2.0 Format
The project uses Feishu's Card 2.0 format with:
- `"schema": "2.0"` declaration
- Markdown elements for content
- Proper structure: header + body with elements

### Current Status
- Stop events show "✅ 任务完成" with green header
- iOS notifications use "任务完成" as title
- Notification events for iOS are currently commented out to reduce noise

## Development Notes

When modifying notification formats or adding new event types, ensure compatibility with:
1. Feishu Card 2.0 JSON structure
2. Bark API URL format for iOS notifications
3. Claude Code's hook data structure