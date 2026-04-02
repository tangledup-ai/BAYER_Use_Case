# 快速打包指南 (Windows)

## 🚀 5分钟快速开始

### 方法一：一键打包（推荐）

1. 双击运行 `build.bat`
2. 等待打包完成（约5-10分钟）
3. 在 `dist\拜耳排班系统\` 目录找到 exe 文件
4. 双击运行即可！

### 方法二：手动打包

如果方法一失败，按以下步骤手动打包：

#### 步骤1：安装工具（仅需一次）

打开命令提示符（CMD），执行：

```bash
# 安装打包工具
pip install pyinstaller

# 验证安装
pyinstaller --version
```

#### 步骤2：执行打包

在项目根目录执行：

```bash
# 使用SPEC文件打包
pyinstaller build.spec --clean

# 或者一行命令搞定
pyinstaller --onefile --windowed --name "拜耳排班系统" --add-data "frontend;frontend" --add-data "backend;backend" run_app.py
```

#### 步骤3：运行测试

打包完成后：

```
dist\
└── 拜耳排班系统\
    ├── 拜耳排班系统.exe      ← 双击运行这个
    ├── 拜耳排班系统.pdb     # 调试文件
    └── _internal\          # 依赖文件
        ├── python.exe
        ├── frontend\        # 前端文件
        ├── backend\        # 后端文件
        └── [其他文件...]
```

## 📋 打包清单

已创建以下打包相关文件：

```
拜耳排班系统/
├── build.bat           ← 一键打包脚本（双击运行）
├── build.spec          ← PyInstaller配置文件
├── run_app.py          ← 应用入口脚本
├── PACKAGING_GUIDE.md   ← 详细打包文档
└── QUICK_START.md      ← 本文档
```

## ⚙️ 打包参数说明

### build.spec 关键配置

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `name` | exe文件名 | `拜耳排班系统` |
| `console` | 是否显示控制台 | `False`（隐藏） |
| `onefile` | 打包成单文件 | `False`（目录模式更稳定） |
| `upx` | 启用UPX压缩 | `True` |
| `debug` | 调试模式 | `False` |

### 命令行参数

```bash
pyinstaller [选项] run_app.py

常用选项：
  --onefile              # 打包成单个exe文件
  --onedir               # 打包成目录（默认）
  --windowed / -w        # 窗口模式，不显示控制台
  --console / -c         # 控制台模式，显示黑窗口
  --name NAME            # 指定输出文件名
  --add-data "SRC;DEST"  # 添加数据文件
  --clean                # 打包前清理
  --debug=all            # 显示详细调试信息
```

## 🔧 常见问题

### Q1: 打包后exe无法运行？

**症状**：双击exe后无反应或立即退出

**解决方案**：
```bash
# 1. 切换到控制台模式查看错误
# 修改build.spec，将 console=False 改为 console=True
pyinstaller build.spec

# 2. 或者使用debug模式
pyinstaller --debug=all run_app.py
```

### Q2: 提示找不到模块？

**症状**：`ModuleNotFoundError: No module named 'xxx'`

**解决方案**：
编辑 `build.spec`，在 `hiddenimports` 列表中添加缺失的模块：

```python
hiddenimports=[
    'flask',
    'flask_cors',
    # 添加缺失的模块
    'your_missing_module',
],
```

然后重新打包：
```bash
pyinstaller build.spec --clean
```

### Q3: 提示找不到前端文件？

**症状**：`找不到 frontend/index.html`

**解决方案**：
1. 检查 `run_app.py` 中的路径是否正确
2. 确保 `frontend` 文件夹与exe在同一目录
3. 检查 `_internal/frontend` 是否存在

### Q4: 杀毒软件报警？

**症状**：exe被识别为病毒

**这是正常现象**：
- PyInstaller打包的程序经常被误报
- 解决方法：
  1. 将exe提交给杀毒软件厂商（360、腾讯管家等）
  2. 使用代码签名证书签名
  3. 信任自己的exe（开发环境）

### Q5: 端口被占用？

**症状**：`Port 5000 is already in use`

**解决方案**：
```bash
# 1. 查找占用端口的进程
netstat -ano | findstr :5000

# 2. 结束该进程（PID替换为实际值）
taskkill /PID 1234 /F

# 3. 或修改run_app.py中的端口
app.run(port=5001)
```

### Q6: 打包时间太长？

**加速方法**：
1. 使用虚拟环境减少依赖
2. 启用UPX压缩
3. 使用Nuitka替代PyInstaller：
```bash
pip install nuitka
python -m nuitka --standalone --onefile run_app.py
```

## 🎨 自定义配置

### 修改应用图标

1. 准备 `.ico` 格式图标文件
2. 放在项目根目录，命名为 `app.ico`
3. 编辑 `build.spec`：
```python
exe = EXE(
    ...,
    icon='app.ico',  # 添加这行
)
```

### 修改应用名称

编辑 `build.spec` 中的 `name` 参数：
```python
name='你的应用名称',
```

### 修改窗口标题

编辑 `run_app.py` 中的HTML文件，或者使用Flask配置：
```python
app.config['Window-Title'] = '拜耳制药排班系统'
```

## 📦 高级打包选项

### 单文件模式（所有文件打包进一个exe）

编辑 `build.spec`：
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='拜耳排班系统',
    onefile=True,  # 添加这行
)
```

**注意**：单文件模式首次运行需要解压，启动较慢。

### 使用虚拟环境

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活环境
venv\Scripts\activate

# 3. 只安装必要的依赖
pip install flask flask-cors pyinstaller

# 4. 执行打包
pyinstaller build.spec --clean
```

## ✅ 验证打包结果

打包成功后，测试以下功能：

- [ ] exe文件可以正常启动
- [ ] 浏览器自动打开应用
- [ ] 所有页面可以正常访问
- [ ] 统计数据正确显示
- [ ] 搜索和筛选功能正常
- [ ] 无控制台错误信息

## 📞 获取帮助

如果遇到其他问题：
1. 查看 `PACKAGING_GUIDE.md` 详细文档
2. 查看上方常见问题解答
3. 检查PyInstaller官方文档

## 🎉 成功案例

恭喜！打包成功后：
- 可以将 `dist\拜耳排班系统` 整个文件夹分享给同事
- 也可以用Inno Setup等工具制作安装程序
- 支持Windows 10/11系统

---

**祝打包成功！** 🚀
