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
