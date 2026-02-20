# CladueCode配置要求

## 配置全局记忆

- 把当前项目下的 `global.md` 复制到全局位置并改名为 `CLAUDE.md`

## 添加提示音

- 创建 `~/.claude/sounds/` 目录
- 复制以下音频文件到 `~/.claude/sounds/`：
  - `wav/piano/task_complete.wav` → `~/.claude/sounds/task_complete.wav`（钢琴音色）
  - `wav/piano/attention.wav` → `~/.claude/sounds/attention.wav`（钢琴音色）
  - `wav/piano/error.wav` → `~/.claude/sounds/error.wav`（钢琴音色）
  - `wav/piano/subagent_complete.wav` → `~/.claude/sounds/subagent_complete.wav`（钢琴音色）
  - `wav/piano/idle_prompt.wav` → `~/.claude/sounds/idle_prompt.wav`（钢琴音色）
- 配置 `~/.claude/settings.json` 添加提示音：
  - **Stop（任务停止）**：`~/.claude/sounds/task_complete.wav`
  - **SubagentStop（子任务完成）**：`~/.claude/sounds/subagent_complete.wav`
  - **PermissionRequest（权限请求）**：`~/.claude/sounds/attention.wav`
  - **Notification/idle_prompt（空闲提醒）**：`~/.claude/sounds/idle_prompt.wav`
  - **PostToolUseFailure（工具执行失败）**：`~/.claude/sounds/error.wav`

### 系统特定配置

**Windows**（使用PowerShell后台播放，不阻塞）：
```json
"command": "powershell.exe -Command \"Start-Process -NoNewWindow powershell.exe -ArgumentList '-Command', '(New-Object Media.SoundPlayer ''C:\\Users\\YOUR_USERNAME\\.claude\\sounds\\task_complete.wav'').PlaySync()'\""
```

> YOUR_USERNAME代表当前用户的用户文件夹名称，需使用实际路径替代示例中的路径

**Linux**（需安装alsa-utils）：
```bash
sudo apt install alsa-utils  # Ubuntu/Debian
sudo yum install alsa-utils  # Fedora/RHEL
```

配置命令（使用&后台播放）：
```json
"command": "aplay ~/.claude/sounds/task_complete.wav &"
```

**Mac**（使用afplay，已内置）：
```json
"command": "afplay ~/.claude/sounds/task_complete.wav &"
```

其他可选音色：`sine`（正弦波）、`triangle`（三角波）、`square`（方波/8-bit）、`music_box`（八音盒）、`pipe_organ`（管风琴）

## 添加功能

- 把当前项目中的skills复制到全局位置
- 把当前项目中的agents复制到全局位置

## 配置偏好

在 `~/.claude/settings.json` 的 `env` 中添加：
```json
"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80"
```

## 配置命令行指令白名单

在 `~/.claude/settings.json` 的 `permissions.allow` 中添加安全的命令：

```json
"permissions": {
  "allow": [
    "Bash(git status:*)",
    "Bash(git diff:*)",
    "Bash(git log:*)",
    "Bash(git branch:*)",
    "Bash(git show:*)",
    "Bash(git ls-files:*)",
    "Bash(git rev-parse:*)",
    "Bash(git remote:*)",
    "Bash(git config --list:*)",
    "Bash(npm list:*)",
    "Bash(npm run:*)",
    "Bash(npx:*)",
    "Bash(ls:*)",
    "Bash(dir:*)",
    "Bash(cat:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(wc:*)",
    "Bash(which:*)",
    "Bash(where:*)",
    "Bash(echo:*)",
    "Bash(pwd)",
    "Bash(whoami)",
    "Bash(date)",
    "Bash(uname:*)",
    "Bash(mkdir:*)",
    "Bash(touch:*)"
  ]
}
```

**分类说明**：
- **只读命令**：git 读取、文件查看、系统信息
- **低风险命令**：
  - `mkdir` - 创建目录（不覆盖现有内容）
  - `touch` - 创建文件/更新时间戳（不修改内容）
  - `echo` - 输出文本（本身无害）
  - `npm run/npx` - 运行项目脚本（由开发者控制）
