# -*- mode: python ; coding: utf-8 -*-
"""
拜耳制药排班系统 - 修复版打包配置
包含所有必要的依赖和hidden imports
"""

import os
import sys

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None
root_dir = os.path.dirname(os.path.abspath(SPEC))

# 收集所有uvicorn相关的数据文件
uvicorn_data = collect_data_files('uvicorn')
starlette_data = collect_data_files('starlette')
pydantic_data = collect_data_files('pydantic')

a = Analysis(
    ['run_app.py'],
    pathex=[root_dir],
    binaries=[],
    datas=[
        # 前端和后端文件
        (os.path.join(root_dir, 'frontend'), 'frontend'),
        (os.path.join(root_dir, 'backend'), 'backend'),
        # 收集的数据文件
        *uvicorn_data,
        *starlette_data,
        *pydantic_data,
    ],
    hiddenimports=[
        # FastAPI及其依赖
        *collect_submodules('fastapi'),
        *collect_submodules('uvicorn'),
        *collect_submodules('pydantic'),
        *collect_submodules('starlette'),
        *collect_submodules('anyio'),
        # 显式添加uvicorn核心模块
        'uvicorn',
        'uvicorn.__main__',
        'uvicorn._utils',
        'uvicorn._constants',
        'uvicorn.config',
        'uvicorn.main',
        'uvicorn.server',
        'uvicorn.workers',
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
        'uvicorn.extensions',
        'uvicorn.extensions.logging',
        # Pydantic核心模块
        'pydantic',
        'pydantic.__init__',
        'pydantic.fields',
        'pydantic.validators',
        'pydantic.main',
        'pydantic.schema',
        'pydantic.dataclasses',
        'pydantic.error_wrappers',
        'pydantic.utils',
        # Starlette核心模块
        'starlette',
        'starlette.__init__',
        'starlette.applications',
        'starlette.routing',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.middleware.gzip',
        'starlette.responses',
        'starlette.requests',
        'starlette.staticfiles',
        'starlette.templating',
        'starlette.websockets',
        # anyio后端
        'anyio',
        'anyio._backends',
        'anyio._backends._asyncio',
        'anyio._backends._trio',
        'anyio.streams',
        'anyio.streams.buffered',
        'anyio.streams.file',
        'anyio.streams.text',
        # 标准库和其他依赖
        'webbrowser',
        'threading',
        'urllib',
        'urllib.request',
        'urllib.error',
        'urllib.parse',
        'json',
        'datetime',
        'collections',
        'typing',
        'asyncio',
        # httptools (uvicorn依赖)
        'httptools',
        'httptools.parser',
        'httptools.http_parser',
        # websockets (uvicorn依赖)
        'websockets',
        'websockets.server',
        'websockets.client',
        'websockets.uri',
        'websockets.frames',
        'websockets.protocol',
        'websockets.handshake',
        # watchfiles (uvicorn依赖)
        'watchfiles',
        'watchfiles._rust',
        # click (uvicorn依赖)
        'click',
        'click.core',
        'click.termui',
        # python-dotenv (uvicorn依赖)
        'dotenv',
        # h11 (uvicorn http核心)
        'h11',
        'h11._abnf',
        'h11._connection',
        'h11._events',
        'h11._state',
        'h11._util',
        'h11._headers',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    name='拜耳排班系统_v3_fixed',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=True,  # 暂时启用控制台以便调试
)
