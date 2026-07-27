#!/usr/bin/env bash
# ============================================================
# AlanDevTeam CLI — Shell 封装
# 安装: echo 'alias alan="bash ~/.zcode/alan-dev-team/alan.sh"' >> ~/.bashrc
# ============================================================

ALAN_CLI="$HOME/.zcode/alan-dev-team/cli/alan.py"

if [ ! -f "$ALAN_CLI" ]; then
    echo "❌ AlanDevTeam 未安装或 CLI 文件缺失"
    echo "   期望路径: $ALAN_CLI"
    exit 1
fi

exec python "$ALAN_CLI" "$@"
