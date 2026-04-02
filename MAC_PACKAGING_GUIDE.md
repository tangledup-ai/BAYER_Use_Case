# Mac 打包 Windows 应用完全指南

## ⚠️ 重要说明

**PyInstaller 不支持在 Mac 上直接交叉编译 Windows 可执行文件！**

在 Mac 上运行的 PyInstaller 只能生成 macOS 的应用包 (.app)，无法直接生成 Windows 的 .exe 文件。

---

## 🎯 解决方案

### 方案1️⃣：GitHub Actions 自动构建（推荐）

在 Mac 上推送代码到 GitHub，自动在 Windows 环境中构建 .exe 文件。

#### 步骤 1：在 GitHub 创建仓库

1. 登录 GitHub: https://github.com
2. 点击 "New repository" 创建新仓库
3. 仓库名称：`bayer-scheduling-system`（或其他名称）
4. 选择 Private 或 Public
5. 点击 "Create repository"

#### 步骤 2：上传代码到 GitHub

在项目根目录执行：

```bash
cd /Volumes/data/baier
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/bayer-scheduling-system.git
git push -u origin main
```

#### 步骤 3：触发 Windows 构建

1. 在 GitHub 仓库页面，点击 "Actions" 标签
2. 点击 "Build Windows Executable" 工作流
3. 点击 "Run workflow"
4. 等待构建完成（约 5-10 分钟）
5. 在 "Artifacts" 中下载 `Windows-Executable-Zip`

#### 步骤 4：获取构建结果

构建成功后：
- 📦 `Windows-Executable.zip` - 完整的 Windows 分发包
- 📁 `Windows-Executable/` - 未压缩的分发目录

#### 步骤 5：在 Windows 上运行

1. 下载并解压 zip 文件
2. 进入 `拜耳排班系统` 文件夹
3. 双击 `拜耳排班系统.exe`
4. 应用启动，自动打开浏览器

---

### 方案2️⃣：VirtualBox + Windows（本地构建）

在 Mac 上安装 Windows 虚拟机，本地构建 .exe 文件。

#### 系统要求

- macOS 10.15+
- 40GB+ 可用磁盘空间
- 8GB+ 内存

#### 安装步骤

1. **下载 VirtualBox**
   ```bash
   brew install --cask virtualbox
   ```

2. **下载 Windows 镜像**
   - 下载 Windows 10/11 ISO: https://www.microsoft.com/software-download/windows11

3. **创建虚拟机**
   - 打开 VirtualBox
   - 点击 "新建"
   - 选择 Windows 10/11 (64-bit)
   - 分配 4GB+ 内存
   - 创建 60GB+ 虚拟硬盘
   - 加载 Windows ISO 并安装

4. **在虚拟机中打包**
   - 安装 Python 3.11+
   - 复制项目文件到虚拟机
   - 安装依赖：`pip install flask flask-cors pyinstaller`
   - 执行打包：`pyinstaller build.spec --clean`

---

### 方案3️⃣：Docker Windows 容器（高级）

使用 Docker 运行 Windows 容器进行构建。

#### 前提条件

- Windows 10/11 Pro + Hyper-V
- 或 Windows Server

#### 步骤

```powershell
# 拉取 Windows Server Core 镜像
docker pull mcr.microsoft.com/windows/servercore:ltsc2022

# 创建构建容器
docker run -it -v C:\path\to\project:/src mcr.microsoft.com/windows/servercore:ltsc2022

# 在容器中安装 Python 和依赖
# 然后执行打包命令
```

---

## ✅ 立即可行的方案

### 现在就可以做：在 Mac 上打包 macOS 应用

```bash
cd /Volumes/data/baier

# 给脚本添加执行权限
chmod +x build_macos.sh

# 运行打包脚本
./build_macos.sh
```

这将生成：
- 📱 `dist/拜耳排班系统.app` - macOS 应用

**使用方法**：
1. 双击运行 `拜耳排班系统.app`
2. 首次运行在系统偏好设置中允许应用运行
3. 应用自动打开浏览器访问系统

---

## 🔄 工作流程建议

### 开发阶段（Mac）

```bash
# 1. 启动后端 API
cd backend
python3 app.py

# 2. 启动前端服务器（另一个终端）
cd frontend
python3 -m http.server 8000

# 3. 浏览器访问 http://localhost:8000
```

### 发布阶段（GitHub Actions）

```bash
# 1. 更新代码
git add .
git commit -m "更新内容"
git push

# 2. GitHub Actions 自动构建 Windows exe
# 3. 下载构建结果
# 4. 分发给用户
```

---

## 📊 各方案对比

| 方案 | 难度 | 耗时 | 成本 | 推荐度 |
|------|------|------|------|--------|
| **GitHub Actions** | ⭐ | 5-10分钟 | 免费 | ⭐⭐⭐⭐⭐ |
| **VirtualBox** | ⭐⭐ | 30-60分钟 | 免费 | ⭐⭐⭐⭐ |
| **Docker Windows** | ⭐⭐⭐ | 20-40分钟 | 免费 | ⭐⭐⭐ |
| **直接Mac打包** | ⭐ | 即时 | 免费 | ⭐⭐⭐ (仅macOS) |

---

## 🎯 推荐的工作流程

### 小团队或个人开发者

1. **使用 GitHub Actions**（免费、自动）
   - 推送代码自动构建
   - 下载 exe 文件分发给用户

2. **保留 macOS 开发环境**
   - 本地开发测试
   - 打包 macOS 版本供 Mac 用户使用

### 企业用户

1. **使用 VirtualBox + Windows**
   - 完全本地化构建
   - 不依赖外部服务
   - 符合安全策略

---

## 📝 常见问题

### Q1: GitHub Actions 需要付费吗？

**不需要**。GitHub 免费账户每月有 2000 分钟的 Actions 时间，足够构建几十个版本。

### Q2: 生成的 exe 文件安全吗？

**安全**。GitHub Actions 在隔离的虚拟机中构建，不会被植入恶意代码。不过杀毒软件可能会误报（这是所有 PyInstaller 打包的程序的常见问题）。

### Q3: 可以构建苹果应用吗？

**可以**。使用 `build_macos.sh` 脚本可以打包 macOS 应用，但需要在 macOS 10.15+ 上运行，且需要代码签名才能分发（否则会有安全警告）。

### Q4: Docker Windows 容器免费吗？

**需要 Windows 授权**。Docker Desktop 在 Windows 上需要 Pro 版本，或者使用 Windows Server。

### Q5: 打包后的文件有多大？

- macOS 应用：约 200-300MB
- Windows exe：约 150-250MB
- 包含 Python 运行时和所有依赖

---

## 🚀 快速开始

### 立即尝试：打包 macOS 版本

```bash
cd /Volumes/data/baier
chmod +x build_macos.sh
./build_macos.sh
```

### 长期方案：设置 GitHub Actions

1. 在 GitHub 创建仓库
2. 推送代码
3. 点击 Actions -> Build Windows Executable -> Run workflow
4. 下载构建结果

---

## 📚 更多资源

- **PyInstaller 文档**: https://pyinstaller.org/en/stable/
- **GitHub Actions 文档**: https://docs.github.com/actions
- **VirtualBox 下载**: https://www.virtualbox.org/wiki/Downloads
- **Windows ISO 下载**: https://www.microsoft.com/software-download/windows11

---

## ✅ 总结

| 你的需求 | 推荐方案 |
|---------|---------|
| Mac 用户，想要 Windows exe | **GitHub Actions** |
| Mac 用户，想要 Mac 应用 | **build_macos.sh** |
| 完全本地化构建 | **VirtualBox + Windows** |
| 追求最新功能 | **本地开发 + GitHub Actions 发布** |

**建议**：现在先用 `build_macos.sh` 打包 macOS 版本，同时创建 GitHub 仓库设置 GitHub Actions 自动构建 Windows 版本。
