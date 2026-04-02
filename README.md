# 拜耳制药排班系统 - 数据分析平台

这是一个使用网页技术开发的本地排班系统，支持Windows APP封装。

## 项目结构

```
baier/
├── frontend/              # 前端代码
│   ├── index.html         # 主页面（数据总览）
│   ├── css/
│   │   └── style.css      # 样式表
│   ├── js/
│   │   └── main.js        # 通用JavaScript函数库
│   └── pages/             # 页面目录
│       ├── leaves.html    # 请假表页面
│       ├── workhours.html # 工时数据页面
│       ├── shifts.html    # 班次数据页面
│       └── positions.html # 岗位工作页面
└── backend/               # 后端代码
    └── app.py             # Flask API服务
```

## 功能特点

### 1. 数据总览页面
- 统计卡片展示关键指标
- 最新数据预览列表
- 快速导航到各数据页面

### 2. 请假表管理
- **数据结构**：姓名 / 请假日期 / 排班请假
- 支持搜索和筛选功能
- 分页展示
- 统计数据（请假总数、请假率等）

### 3. 工时数据管理
- **数据结构**：姓名 / 员工ID / 已有工时
- 支持按工时排序
- 进度条可视化展示
- 统计数据（总工时、平均工时等）

### 4. 班次数据管理
- **数据结构**：姓名 / 班次 / 个人班次数 / 总班次数 / 个人班次比例 / 历史班次比例
- 支持按班次类型筛选
- 双进度条对比展示（个人比例 vs 历史比例）
- 统计数据（总班次数、平均比例等）

### 5. 岗位工作管理
- **数据结构**：岗位ID / 个人班次 / 岗位班次 / 期望工作占比
- 分配均衡度分析
- 可视化占比展示
- 统计数据（岗位总数、均衡度评分等）

## 技术栈

### 前端
- HTML5 + CSS3
- JavaScript (ES6+)
- 响应式设计
- 现代渐变色彩

### 后端
- Python 3.x
- Flask Web框架
- Flask-CORS (跨域支持)

## 安装和运行

### 前端运行

1. 使用任意Web服务器托管前端文件，例如：
   ```bash
   # 使用Python内置服务器
   cd frontend
   python -m http.server 8000
   ```

2. 或直接双击 `frontend/index.html` 在浏览器中打开

### 后端API运行

1. 安装依赖：
   ```bash
   pip install flask flask-cors
   ```

2. 启动服务器：
   ```bash
   cd backend
   python app.py
   ```

3. API服务将在 http://localhost:5000 上运行

## API接口

### 仪表板统计
- `GET /api/dashboard/stats` - 获取统计数据

### 请假管理
- `GET /api/leaves` - 获取请假列表
- `POST /api/leaves` - 创建请假记录

### 工时管理
- `GET /api/workhours` - 获取工时列表
- `POST /api/workhours` - 创建工时记录

### 班次管理
- `GET /api/shifts` - 获取班次列表
- `POST /api/shifts` - 创建班次记录

### 岗位管理
- `GET /api/positions` - 获取岗位列表
- `POST /api/positions` - 创建岗位记录

## 数据结构

### 请假表
```json
{
  "name": "张三",
  "date": "2026-04-01",
  "scheduled": "是"
}
```

### 工时数据
```json
{
  "name": "张三",
  "id": "EMP001",
  "hours": 168,
  "month": "2026-04"
}
```

### 班次数据
```json
{
  "name": "张三",
  "shift": "早班",
  "personalShifts": 15,
  "totalShifts": 20,
  "personalRatio": 75.0,
  "historicalRatio": 70.0
}
```

### 岗位工作
```json
{
  "positionId": "P001",
  "personalShifts": 20,
  "positionShifts": 45,
  "expectedRatio": 44.4,
  "month": "2026-04"
}
```

## 开发说明

### 前端开发
- 所有页面使用统一的 `style.css` 样式
- 通用函数库 `main.js` 提供工具函数
- 支持响应式设计，适配移动端

### 后端开发
- RESTful API设计
- CORS跨域支持
- 错误处理机制
- 数据验证

### 扩展建议
1. **数据库集成**：当前使用内存存储，建议集成MySQL/PostgreSQL
2. **用户认证**：添加登录和权限管理
3. **数据导入导出**：支持Excel/CSV导入导出
4. **图表可视化**：集成ECharts或Chart.js
5. **实时更新**：使用WebSocket实现数据实时更新

## 浏览器兼容性

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 许可证

本项目仅供学习交流使用。

## 联系方式

如有问题或建议，请联系开发团队。
