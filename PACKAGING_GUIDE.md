# Windows EXE 打包指南

## 打包方案

本项目使用 **PyInstaller** 将Python Flask应用打包成Windows可执行文件。

## 前置要求

1. Windows 10/11 系统
2. Python 3.8+ 已安装
3. 良好的网络连接（下载依赖）

## 打包步骤

### 第一步：安装打包工具

```bash
# 安装PyInstaller
pip install pyinstaller

# 安装UPX（可选，用于减小文件大小）
# 从 https://upx.github.io/ 下载并添加到PATH
```

### 第二步：创建启动脚本

项目已包含 `run_app.py` 作为启动入口。

### 第三步：执行打包

在项目根目录执行：

```bash
# 方法1：使用命令行打包
pyinstaller --onefile --windowed --name "拜耳排班系统" --add-data "frontend;frontend" run_app.py

# 方法2：使用SPEC文件（推荐）
pyinstaller build.spec
```

### 第四步：运行exe

打包完成后，exe文件位于 `dist/` 目录：

```
dist/
└── 拜耳排班系统.exe  # 双击运行
```

## 打包配置说明

### SPEC文件配置 (build.spec)

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 分析主程序
a = Analysis(
    ['run_app.py'],           # 入口脚本
    pathex=[],                # 额外路径
    binaries=[],              # 二进制文件
    datas=[
        ('frontend', 'frontend'),  # 包含前端文件
    ],                        # 附加数据文件
    hiddenimports=[           # 隐藏导入（重要！）
        'flask',
        'flask_cors',
        'werkzeug',
        'jinja2',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 生成可执行文件
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 打包模式
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='拜耳排班系统',           # exe文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,            # True=显示控制台，False=隐藏（窗口模式）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# 收集所有文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='拜耳排班系统',
)
```

## 启动脚本说明

`run_app.py` 完成了以下工作：

1. **获取程序所在目录** - 无论从哪个位置运行，都能正确定位文件
2. **配置前端文件路径** - 确保Flask能找到HTML/CSS/JS文件
3. **启动Flask服务器** - 在本地端口运行Web服务
4. **自动打开浏览器** - 打开默认浏览器访问应用
5. **优雅退出** - 支持Ctrl+C或关闭窗口时安全退出

## 打包后文件结构

```
dist/
└── 拜耳排班系统/
    ├── 拜耳排班系统.exe      # 主程序
    ├── _internal/            # 依赖库
    │   ├── python.exe
    │   ├── flask/
    │   ├── frontend/        # 前端文件
    │   └── ...（其他依赖）
    └── README.txt           # 使用说明
```

## 高级配置

### 添加应用图标

1. 准备图标文件（.ico格式）
2. 在SPEC文件中添加：

```python
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='拜耳排班系统',
    icon='app.ico',          # 添加这行
    console=False,
)
```

### 减小文件大小

1. 使用虚拟环境只安装必要依赖
2. 启用UPX压缩
3. 排除不需要的模块

```bash
pyinstaller --onefile --windowed \
    --name "拜耳排班系统" \
    --add-data "frontend;frontend" \
    --exclude-module tkinter \
    --exclude-module test \
    run_app.py
```

### 添加版本信息

在Windows上，可以添加版本信息文件（version_info.txt）：

```python
exe = EXE(
    pyz,
    a.scripts,
    [],
    name='拜耳排班系统',
    version='version_info.txt',  # Windows版本信息
)
```

## 常见问题

### 1. 打包失败或exe无法运行

**问题**：提示缺少模块或打包后无法启动

**解决方案**：
- 检查 `hiddenimports` 是否包含所有使用的模块
- 查看打包日志中的警告信息
- 使用 `--debug=all` 参数重新打包查看详细错误

```bash
pyinstaller --onefile --debug=all run_app.py
```

### 2. 前端文件找不到

**问题**：运行时提示找不到HTML文件

**解决方案**：
- 确保 `run_app.py` 中的路径正确
- 确认打包时 `--add-data` 参数正确
- 检查 `_internal/frontend` 目录是否存在

### 3. 端口被占用

**问题**：提示端口5000已被占用

**解决方案**：
- 修改 `run_app.py` 中的端口号
- 或在运行前关闭占用端口的程序

### 4. 杀毒软件误报

**问题**：exe被杀毒软件标记

**解决方案**：
- 这是常见现象，PyInstaller打包的程序经常被误报
- 可以提交给杀毒软件厂商进行白名单申请
- 使用代码签名证书签名（需要购买）

### 5. 窗口一闪而过

**问题**：exe运行后窗口立即关闭

**解决方案**：
- 修改SPEC文件设置 `console=True` 查看错误信息
- 或在 `run_app.py` 中添加错误捕获

## 性能优化建议

1. **使用Nuitka替代PyInstaller**
   ```bash
   pip install nuitka
   python -m nuitka --standalone --onefile run_app.py
   ```
   Nuitka将Python编译成C，性能更好，但打包时间更长。

2. **清理不必要的依赖**
   - 创建虚拟环境只安装必要包
   - 使用 `pipreqs` 自动生成requirements.txt

3. **启用UPX压缩**
   - 下载UPX并添加到系统PATH
   - PyInstaller会自动使用UPX压缩

## 完整打包脚本

为简化打包过程，项目提供了自动化脚本：

```bash
# Windows PowerShell
.\build.bat
```

或手动执行：
```bash
# 1. 安装依赖
pip install -r backend/requirements.txt
pip install pyinstaller

# 2. 执行打包
pyinstaller build.spec

# 3. 测试exe
.\dist\拜耳排班系统\拜耳排班系统.exe
```

## 注意事项

1. **打包路径** - 避免使用中文路径，可能导致问题
2. **Python版本** - 确保开发环境和打包环境Python版本一致
3. **依赖完整** - 所有使用的库都必须在requirements.txt中
4. **测试充分** - 在干净的环境中测试exe文件

## 卸载

删除 `dist` 目录即可完全卸载打包的文件。
