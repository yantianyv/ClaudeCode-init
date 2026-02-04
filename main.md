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

- 修改自动压缩提示词的阈值为80%
