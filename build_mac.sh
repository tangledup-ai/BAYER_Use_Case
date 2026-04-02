#!/bin/bash
###############################################################################
# 拜耳制药排班系统 - Mac交叉编译Windows打包脚本
# Cross-compile Windows executable on Mac
###############################################################################

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "  Bayer Scheduling System - Mac Build Tool"
echo "=========================================="
echo ""

# 进度显示函数
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

###############################################################################
# 第1步：检查和安装依赖
###############################################################################
print_step "1/4 - 检查系统环境..."

# 检查macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "此脚本仅支持 macOS 系统"
    exit 1
fi

print_success "操作系统: macOS $(sw_vers -productVersion)"

# 检查Homebrew
if ! command_exists brew; then
    print_warning "Homebrew 未安装，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

print_success "Homebrew 已安装"

# 检查Python
if ! command_exists python3; then
    print_error "Python 3 未安装，请先安装Python"
    echo "  brew install python3"
    exit 1
fi

print_success "Python: $(python3 --version)"

# 检查pip
if ! command_exists pip3; then
    print_warning "pip3 未安装，正在安装..."
    python3 -m ensurepip --upgrade
fi

print_success "pip3 已就绪"

###############################################################################
# 第2步：安装交叉编译工具
###############################################################################
print_step "2/4 - 安装交叉编译工具..."

# 安装PyInstaller
print_step "安装 PyInstaller..."
pip3 install --user pyinstaller

if command_exists pyinstaller; then
    print_success "PyInstaller: $(pyinstaller --version)"
else
    print_warning "PyInstaller 安装到用户目录，添加到PATH..."
    export PATH="$HOME/Library/Python/3.*/bin:$PATH"
fi

# 安装前置依赖
print_step "安装项目依赖..."
pip3 install flask flask-cors

print_success "所有依赖安装完成"

###############################################################################
# 第3步：清理旧的构建文件
###############################################################################
print_step "3/4 - 清理旧构建文件..."

# 清理build和dist目录
if [ -d "build" ]; then
    print_warning "删除旧的 build 目录..."
    rm -rf build
fi

if [ -d "dist" ]; then
    print_warning "删除旧的 dist 目录..."
    rm -rf dist
fi

print_success "清理完成"

###############################################################################
# 第4步：执行打包
###############################################################################
print_step "4/4 - 执行 Windows 交叉编译..."

# 创建Windows SPEC文件（使用UTF-8编码）
cat > build_windows.spec << 'SPECEOF'
# -*- mode: python ; coding: utf-8 -*-
"""
Bayer Scheduling System - Windows Build Specification
Cross-compiled on macOS
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
        'markupsafe',
        'itsdangerous',
        'click',
        'webbrowser',
        'threading',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'unittest', 'pytest', 'pdb', 'doctest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='拜耳排班系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # macOS上关闭UPX
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='拜耳排班系统',
    console=False,
)
SPECEOF

print_warning "注意: 这是交叉编译，只能在Windows系统上运行！"
echo ""

# 执行PyInstaller打包
echo "开始打包，请耐心等待..."
echo "=========================================="

# 使用Python3明确执行pyinstaller
python3 -m PyInstaller build_windows.spec --clean --noconfirm

echo "=========================================="
echo ""

###############################################################################
# 完成
###############################################################################
if [ -f "dist/拜耳排班系统/拜耳排班系统.exe" ]; then
    print_success "打包成功！"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  📦 Windows可执行文件已生成"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📁 文件位置："
    echo "   $PROJECT_ROOT/dist/拜耳排班系统/拜耳排班系统.exe"
    echo ""
    echo "📦 完整分发包："
    echo "   $PROJECT_ROOT/dist/拜耳排班系统/"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # 显示文件大小
    if command_exists du; then
        SIZE=$(du -sh "dist/拜耳排班系统" | cut -f1)
        print_success "打包大小: $SIZE"
    fi

    echo ""
    print_warning "下一步操作："
    echo "  1. 将 dist/拜耳排班系统/ 文件夹复制到Windows电脑"
    echo "  2. 双击 '拜耳排班系统.exe' 运行"
    echo "  3. 享受您的排班系统！"
    echo ""

else
    print_error "打包失败！"
    echo ""
    echo "请检查以下可能的问题："
    echo "  1. 依赖是否全部安装"
    echo "  2. run_app.py 是否存在"
    echo "  3. frontend 和 backend 目录是否完整"
    echo ""
    echo "尝试手动执行："
    echo "  python3 -m PyInstaller build_windows.spec --debug=all"
    echo ""
    exit 1
fi

# 清理临时SPEC文件
if [ -f "build_windows.spec" ]; then
    rm -f build_windows.spec
fi

print_success "构建脚本执行完成！"
