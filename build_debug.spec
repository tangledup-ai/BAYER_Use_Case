# -*- mode: python ; coding: utf-8 -*-
"""
拜耳制药排班系统 - 调试版打包配置
启用控制台以便查看错误信息
"""

import os
import sys

from PyInstaller.utils.hooks import collect_submodules

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
        *collect_submodules('fastapi'),
        *collect_submodules('uvicorn'),
        *collect_submodules('pydantic'),
        *collect_submodules('starlette'),
        *collect_submodules('anyio'),
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
    name='拜耳排班系统_debug',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
