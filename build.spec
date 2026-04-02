# -*- mode: python ; coding: utf-8 -*-
"""
拜耳制药排班系统 - PyInstaller打包配置
用于将Python FastAPI应用打包成Windows可执行文件
"""

import os
import sys

# PyInstaller通用导入
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 获取项目根目录
root_dir = os.path.dirname(os.path.abspath(SPEC))

# 分析依赖
a = Analysis(
    # 入口脚本
    ['run_app.py'],

    # 额外路径
    pathex=[root_dir],

    # 二进制文件
    binaries=[],

    # 附加数据文件 - 包含前端文件
    datas=[
        # 格式: ('源路径', '目标目录名')
        # 前端文件将被打包到 frontend/ 目录下
        (os.path.join(root_dir, 'frontend'), 'frontend'),
    ],

    # 隐藏导入 - 确保这些模块被打包
    hiddenimports=[
        *collect_submodules('fastapi'),
        *collect_submodules('uvicorn'),
        *collect_submodules('pydantic'),
        *collect_submodules('starlette'),
        *collect_submodules('anyio'),
        # 标准库模块
        'webbrowser',
        'threading',
        'urllib',
        'json',
        'datetime',
    ],

    # Hook路径
    hookspath=[],

    # 运行时钩子
    runtime_hooks=[],

    # 排除的模块
    excludes=[
        'tkinter',      # GUI库，打包CLI应用时排除
        'test',         # 测试模块
        'unittest',     # 单元测试
        'pytest',       # 测试框架
        'pdb',          # 调试器
        'doctest',      # 文档测试
    ],

    # Windows特定配置
    win_no_prefer_redirects=False,
    win_private_assemblies=False,

    # 加密设置
    cipher=block_cipher,

    # 不使用存档
    noarchive=False,
)

# 收集所有数据文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建单文件可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='拜耳排班系统_v3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,  # 设置为True以显示控制台窗口，方便调试

)
