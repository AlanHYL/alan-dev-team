#!/usr/bin/env bash
# ============================================================
# AlanDevTeam — 一键安装脚本
# 用法: bash <(curl -s https://raw.githubusercontent.com/AlanHYL/alan-dev-team/main/install.sh)
#    或者: git clone https://github.com/AlanHYL/alan-dev-team.git && cd alan-dev-team && bash install.sh
# ============================================================

set -e

REPO_URL="https://github.com/AlanHYL/alan-dev-team.git"
INSTALL_DIR="$HOME/.zcode/alan-dev-team"
ALAN_CMD="$HOME/.zcode/alan-dev-team/alan.sh"

echo "========================================"
echo "  AlanDevTeam — 一键安装"
echo "========================================"
echo ""

# 安装目录
if [ -d "$INSTALL_DIR" ]; then
    echo "[1/3] 更新已有安装..."
    cd "$INSTALL_DIR" && git pull
else
    echo "[1/3] 克隆仓库..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 配置 alan 命令
echo "[2/3] 配置 alan 命令..."

# Git Bash / Linux / macOS
if ! grep -q "alan-dev-team" ~/.bashrc 2>/dev/null; then
    echo "alias alan=\"bash \$HOME/.zcode/alan-dev-team/alan.sh\"" >> ~/.bashrc
    echo "  ✅ 已添加到 ~/.bashrc"
fi

# Zsh (macOS)
if [ -f ~/.zshrc ] && ! grep -q "alan-dev-team" ~/.zshrc 2>/dev/null; then
    echo "alias alan=\"bash \$HOME/.zcode/alan-dev-team/alan.sh\"" >> ~/.zshrc
    echo "  ✅ 已添加到 ~/.zshrc"
fi

# 验证
echo "[3/3] 验证安装..."
python "$INSTALL_DIR/cli/alan.py" doctor 2>&1 | tail -5

echo ""
echo "========================================"
echo "  ✅ AlanDevTeam 安装完成！"
echo "========================================"
echo ""
echo "重新打开终端，或运行:"
echo "  source ~/.bashrc"
echo ""
echo "然后试试:"
echo "  alan init my-project --type web-flask"
echo "  alan start ./my-project"
echo "  alan team"
echo "  alan tutorial"
echo ""
