#!/bin/bash
###############################################################################
# 拜耳制药排班系统 - macOS 打包脚本
# Build macOS Application Bundle
###############################################################################

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  拜耳制药排班系统 - macOS 打包工具${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

print_step() { echo -e "${BLUE}[STEP]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# 检查环境
print_step "检查系统环境..."
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "此脚本仅支持 macOS 系统"
    exit 1
fi

print_success "macOS $(sw_vers -productVersion) - $(sw_vers -productName)"
print_success "检测到 macOS 系统，开始打包..."

# 清理旧文件
print_step "清理旧的构建文件..."
[ -d "build" ] && rm -rf build
[ -d "dist" ] && rm -rf dist
print_success "清理完成"

# 创建 macOS SPEC 文件
print_step "创建打包配置..."

cat > build_macos.spec << 'SPECEOF'
# -*- mode: python ; coding: utf-8 -*-
"""
Bayer Scheduling System - macOS Build Specification
"""

import os
import sys

block_cipher = None
root_dir = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    ['run_app.py'],
    pathex=[root_dir],
    binaries=[],
    datas=[
        (os.path.join(root_dir, 'frontend'), 'frontend'),
        (os.path.join(root_dir, 'backend'), 'backend'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'werkzeug',
        'jinja2',
        'webbrowser',
        'threading',
    ],
    hookspath=[],
    excludes=['tkinter', 'test', 'unittest'],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='拜耳排班系统',
    debug=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='拜耳排班系统',
    appname='拜耳排班系统',
    version='1.0.0',
)
SPECEOF

# 执行打包
print_step "开始打包 macOS 应用..."
echo ""
python3 -m PyInstaller build_macos.spec --clean --noconfirm

echo ""
print_success "打包完成！"

# 检查结果 - 修正检查逻辑
DIST_PATH="$PROJECT_ROOT/dist/拜耳排班系统"

if [ -d "$DIST_PATH" ]; then
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ macOS 应用打包成功！${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "📁 应用位置："
    echo "   $DIST_PATH"
    echo ""
    echo -e "📦 完整分发包："
    echo "   $PROJECT_ROOT/dist/"
    echo ""

    # 显示主程序信息
    if [ -f "$DIST_PATH/拜耳排班系统" ]; then
        SIZE=$(ls -lh "$DIST_PATH/拜耳排班系统" | awk '{print $5}')
        print_success "主程序大小: $SIZE"

        # 显示完整目录大小
        TOTAL_SIZE=$(du -sh "$DIST_PATH" 2>/dev/null | cut -f1)
        print_success "完整分发包大小: $TOTAL_SIZE"
    fi

    echo ""
    print_warning "使用说明："
    echo "   1. 进入 dist/拜耳排班系统 目录"
    echo "   2. 双击 '拜耳排班系统' 可执行文件运行"
    echo "   3. 应用将自动打开浏览器访问系统"
    echo ""
    echo "   或者在终端运行："
    echo "   open \"$DIST_PATH/拜耳排班系统\""
    echo ""

    # 清理临时文件
    rm -f build_macos.spec

    print_success "✅ macOS 打包完成！"

    # 询问是否立即运行
    echo ""
    read -p "是否立即运行应用？ (Y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在启动应用..."
        open "$DIST_PATH"
    fi

else
    print_error "打包失败！"
    echo ""
    echo "请检查以下可能的问题："
    echo "  1. 依赖是否全部安装"
    echo "  2. run_app.py 是否存在"
    echo "  3. frontend 和 backend 目录是否完整"
    echo ""
    echo "尝试手动执行："
    echo "  python3 -m PyInstaller build_macos.spec --debug=all"
    echo ""
    rm -f build_macos.spec
    exit 1
fi
