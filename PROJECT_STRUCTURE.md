# 拜耳制药排班系统 - 完整项目结构

```
拜耳制药排班系统/
│
├── 📄 核心应用文件
│   ├── run_app.py              # 应用启动入口（打包用）
│   ├── build.spec              # PyInstaller打包配置
│   ├── build.bat               # Windows一键打包脚本
│   │
│   ├── requirements.txt         # 项目依赖清单
│   ├── README.md               # 项目说明文档
│   ├── PACKAGING_GUIDE.md       # 详细打包指南
│   └── QUICK_START.md          # 快速开始指南
│
├── 🌐 前端代码 (frontend/)
│   ├── index.html              # 数据总览主页
│   ├── css/
│   │   └── style.css          # 统一样式表
│   ├── js/
│   │   └── main.js           # 通用工具函数库
│   └── pages/                 # 页面目录
│       ├── leaves.html        # 请假表页面
│       ├── workhours.html     # 工时数据页面
│       ├── shifts.html        # 班次数据页面
│       └── positions.html     # 岗位工作页面
│
└── ⚙️ 后端代码 (backend/)
    ├── app.py                 # Flask API服务
    └── requirements.txt       # 后端依赖清单


📦 打包输出目录 (dist/)
└── 拜耳排班系统/
    ├── 拜耳排班系统.exe        # 主程序 ← 双击运行
    ├── _internal/             # 依赖库
    │   ├── python.exe
    │   ├── frontend/         # 前端文件（自动包含）
    │   ├── backend/          # 后端文件（自动包含）
    │   └── [其他依赖...]
    └── README.txt           # 使用说明


🛠️ 打包工具文件
├── build/                    # 打包过程文件（自动生成）
└── __pycache__/             # Python缓存（自动生成）
```

## 📚 文档说明

| 文档 | 用途 | 目标读者 |
|------|------|---------|
| `README.md` | 项目整体介绍 | 所有用户 |
| `QUICK_START.md` | 5分钟快速打包 | 开发者 |
| `PACKAGING_GUIDE.md` | 详细打包文档 | 高级用户 |
| `frontend/README.md` | 前端使用说明 | 前端开发者 |

## 🚀 快速开始

### 开发模式
```bash
# 启动后端API
cd backend
pip install -r requirements.txt
python app.py

# 启动前端（另一个终端）
cd frontend
python -m http.server 8000
# 浏览器访问 http://localhost:8000
```

### 打包成EXE
```bash
# Windows系统，双击运行
build.bat

# 或手动执行
pyinstaller build.spec --clean
```

## 📊 数据结构对照表

### 1. 请假表
```
姓名 | 请假日期 | 排班请假
张三 | 2026-04-01 | 是
李四 | 2026-04-02 | 否
```

### 2. 工时数据
```
姓名 | 员工ID | 已有工时
赵六 | EMP001 | 168小时
孙七 | EMP002 | 160小时
```

### 3. 班次数据
```
姓名 | 班次 | 个人次数 | 总次数 | 个人比例 | 历史比例
钱一 | 早班 | 15 | 20 | 75% | 70%
孙二 | 中班 | 18 | 22 | 81.8% | 75%
```

### 4. 岗位工作
```
岗位ID | 个人班次 | 岗位班次 | 期望占比
P001 | 20 | 45 | 44.4%
P002 | 15 | 30 | 50%
```

## ✨ 功能特性

### 前端功能
- 📊 数据总览仪表板
- 🔍 多条件搜索筛选
- 📄 数据表格分页展示
- 📈 进度条可视化
- 🎨 响应式设计
- 🌐 浏览器自动启动

### 后端功能
- RESTful API设计
- 跨域支持（CORS）
- 数据验证
- 错误处理
- 示例数据

## 🔧 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端框架 | HTML5 + CSS3 + JavaScript | ES6+ |
| 后端框架 | Python Flask | 2.0+ |
| 打包工具 | PyInstaller | 5.0+ |
| 数据库 | 内存存储 | - |
| 协议 | HTTP | 1.1 |

## 💻 系统要求

### 开发环境
- Python 3.8+
- pip包管理器
- Web浏览器

### 运行环境（打包后）
- Windows 10/11
- 无需Python环境
- 无需管理员权限
- 500MB磁盘空间

## 📦 打包大小估算

| 组件 | 大小 |
|------|------|
| Python运行时 | ~150MB |
| Flask依赖 | ~30MB |
| 前端文件 | ~5MB |
| **总计** | **~200MB** |

## 🎯 常见应用场景

1. **本地部署**：不依赖云服务器
2. **数据安全**：数据存储在本地
3. **离线使用**：无需网络连接
4. **快速启动**：双击即可运行
5. **便捷分享**：打包文件夹直接分发

## 📞 技术支持

- 查看 `QUICK_START.md` 快速开始
- 查看 `PACKAGING_GUIDE.md` 详细指南
- 查看各文件内注释文档
