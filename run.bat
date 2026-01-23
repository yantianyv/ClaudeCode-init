@echo off
chcp 65001 >nul
echo 正在启动 Claude Code 并加载配置任务...
echo.

REM 复制配置任务到剪贴板
powershell.exe -Command "Get-Content '%~dp0main.md' -Encoding UTF8 | Set-Clipboard"

echo [配置任务已复制到剪贴板，在 Claude Code 中粘贴即可]
echo.
echo ========================================
type "%~dp0main.md"
echo ========================================
echo.

REM 启动 Claude Code
claude
