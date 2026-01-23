#!/bin/bash
echo "正在启动 Claude Code 并加载配置任务..."
echo

# 复制配置任务到剪贴板（Mac）
if [[ "$OSTYPE" == "darwin"* ]]; then
  pbcopy < "$(dirname "$0")/main.md"
  echo "[配置任务已复制到剪贴板，在 Claude Code 中粘贴即可]"
# 复制配置任务到剪贴板（Linux，需要 xclip）
elif command -v xclip &> /dev/null; then
  xclip -selection clipboard < "$(dirname "$0")/main.md"
  echo "[配置任务已复制到剪贴板，在 Claude Code 中粘贴即可]"
else
  echo "[提示：请手动复制下方内容]"
fi
echo
echo ========================================
cat "$(dirname "$0")/main.md"
echo ========================================
echo

# 启动 Claude Code
claude
