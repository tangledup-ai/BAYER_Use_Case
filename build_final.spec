# -*- mode: python ; coding: utf-8 -*-
"""
拜耳制药排班系统 - 最终打包配置
Console=False，适合最终用户分发
"""

import os
import sys

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None
root_dir = os.path.dirname(os.path.abspath(SPEC))

uvicorn_data = collect_data_files('uvicorn')
starlette_data = collect_data_files('starlette')
pydantic_data = collect_data_files('pydantic')

a = Analysis(
    ['run_app.py'],
    pathex=[root_dir],
    binaries=[],
    datas=[
        (os.path.join(root_dir, 'frontend'), 'frontend'),
        (os.path.join(root_dir, 'backend'), 'backend'),
        *uvicorn_data,
        *starlette_data,
        *pydantic_data,
    ],
    hiddenimports=[
        *collect_submodules('fastapi'),
        *collect_submodules('uvicorn'),
        *collect_submodules('pydantic'),
        *collect_submodules('starlette'),
        *collect_submodules('anyio'),
        'uvicorn',
        'uvicorn.__main__',
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
        'pydantic',
        'pydantic.fields',
        'pydantic.validators',
        'starlette',
        'starlette.applications',
        'starlette.routing',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.responses',
        'starlette.requests',
        'anyio',
        'anyio._backends',
        'anyio._backends._asyncio',
        'anyio._backends._trio',
        'webbrowser',
        'threading',
        'urllib',
        'json',
        'datetime',
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
    name='拜耳排班系统_v4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False,
)
