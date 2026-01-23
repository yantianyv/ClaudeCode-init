# CladueCode配置要求

## 配置全局记忆

- 把当前项目下的 `global.md` 复制到全局位置并改名为 `CLAUDE.md`

## 添加提示音

- 创建 `~/.claude/sounds/` 目录
- 复制项目 `wav/` 目录下的音频文件到 `~/.claude/sounds/`
- 配置 `~/.claude/settings.json` 添加提示音：
  - **Stop（任务停止）**：`~/.claude/sounds/task_complete.wav`
  - **PermissionRequest（权限请求）**：`~/.claude/sounds/attention.wav`
  - **PostToolUseFailure（工具执行失败）**：`~/.claude/sounds/error.wav`

根据当前系统安装音频播放工具（Windows自带PowerShell，Mac自带afplay，Linux需安装aplay）

## 添加功能

- 把当前项目中的skills复制到全局位置
- 把当前项目中的agents复制到全局位置

## 配置偏好

- 修改自动压缩提示词的阈值为80%
