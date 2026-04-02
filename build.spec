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
        (os.path.join(root_dir, 'backend'), 'backend'),
    ],

    # 隐藏导入 - 确保这些模块被打包
    hiddenimports=[
        # FastAPI核心模块
        'fastapi',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',

        # Pydantic模块
        'pydantic',
        'pydantic.fields',
        'pydantic.validators',
        'pydantic.main',
        'pydantic.basemodel',

        # Starlette模块（FastAPI依赖）
        'starlette',
        'starlette.applications',
        'starlette.routing',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.responses',
        'starlette.requests',

        # AnyIO模块（异步支持）
        'anyio',
        'anyio.to_process',

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

# 创建可执行文件
exe = EXE(
    # Python模块归档
    pyz,

    # 脚本文件
    a.scripts,

    # 二进制文件
    [],

    # 排除二进制文件到单独目录
    exclude_binaries=True,

    # 可执行文件名（Windows下会添加.exe后缀）
    name='拜耳排班系统',

    # 调试模式
    debug=False,

    # 启动脚本去除签名
    bootloader_ignore_signals=False,

    # 去除符号表
    strip=False,

    # 使用UPX压缩
    upx=False,

    # 控制台模式
    # False = 窗口模式（不显示控制台窗口）
    # True = 控制台模式（显示黑色控制台窗口）
    console=False,

    # 窗口图标（可选）
    # icon='app.ico',

    # 禁用窗口化回溯
    disable_windowed_traceback=False,

    # argv模拟
    argv_emulation=False,

    # 目标架构
    target_arch=None,

    # 代码签名
    codesign_identity=None,

    # 权限文件
    entitlements_file=None,
)

# 收集所有文件到输出目录
coll = COLLECT(
    # 可执行文件
    exe,

    # 二进制文件
    a.binaries,

    # ZIP文件
    a.zipfiles,

    # 数据文件
    a.datas,

    # 去除符号表
    strip=False,

    # 使用UPX压缩
    upx=False,

    # UPX排除列表
    upx_exclude=[],

    # 输出目录名
    name='拜耳排班系统',

    # 目录模式（True = 创建单文件夹，False = 扁平结构）
    # 建议保持False，因为有些依赖需要目录结构
    console=False,
)
