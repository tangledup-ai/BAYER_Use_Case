"""
拜耳制药排班系统 - 后端API服务
使用FastAPI框架提供RESTful API接口
"""

from fastapi import FastAPI, HTTPException, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import os


app = FastAPI(
    title="拜耳制药排班系统 API",
    description="拜耳制药排班系统的RESTful API接口",
    version="1.0.0"
)

# 配置CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic模型定义
class LeaveCreate(BaseModel):
    """请假记录创建模型"""
    name: str = Field(..., description="员工姓名")
    date: str = Field(..., description="请假日期")
    scheduled: str = Field(..., description="是否已安排排班")


class WorkHourCreate(BaseModel):
    """工时记录创建模型"""
    name: str = Field(..., description="员工姓名")
    id: str = Field(..., description="员工ID")
    hours: float = Field(..., description="工时数")
    month: str = Field(..., description="月份")


class ShiftCreate(BaseModel):
    """班次记录创建模型"""
    name: str = Field(..., description="员工姓名")
    shift: str = Field(..., description="班次类型")
    personalShifts: int = Field(..., description="个人班次数")
    totalShifts: int = Field(..., description="总班次数")
    historicalRatio: Optional[float] = Field(None, description="历史比例")


class PositionCreate(BaseModel):
    """岗位记录创建模型"""
    positionId: str = Field(..., description="岗位ID")
    personalShifts: int = Field(..., description="个人班次数")
    positionShifts: int = Field(..., description="岗位总班次数")
    month: Optional[str] = Field(None, description="月份")


# 模拟数据存储
# 实际项目中应使用数据库（如MySQL、PostgreSQL、MongoDB等）

# 请假数据
leaves_data = [
    {"name": "张三", "date": "2026-04-01", "scheduled": "是"},
    {"name": "李四", "date": "2026-04-02", "scheduled": "否"},
    {"name": "王五", "date": "2026-04-03", "scheduled": "是"},
    {"name": "赵六", "date": "2026-04-05", "scheduled": "是"},
    {"name": "孙七", "date": "2026-04-06", "scheduled": "否"},
    {"name": "周八", "date": "2026-04-08", "scheduled": "是"},
    {"name": "吴九", "date": "2026-04-10", "scheduled": "否"},
    {"name": "郑十", "date": "2026-04-12", "scheduled": "是"},
]

# 工时数据
workhours_data = [
    {"name": "赵六", "id": "EMP001", "hours": 168, "month": "2026-04"},
    {"name": "孙七", "id": "EMP002", "hours": 160, "month": "2026-04"},
    {"name": "周八", "id": "EMP003", "hours": 152, "month": "2026-04"},
    {"name": "吴九", "id": "EMP004", "hours": 144, "month": "2026-04"},
    {"name": "郑十", "id": "EMP005", "hours": 136, "month": "2026-04"},
]

# 班次数据
shifts_data = [
    {"name": "钱一", "shift": "早班", "personalShifts": 15, "totalShifts": 20, "personalRatio": 75, "historicalRatio": 70},
    {"name": "孙二", "shift": "中班", "personalShifts": 18, "totalShifts": 22, "personalRatio": 81.8, "historicalRatio": 75},
    {"name": "李三", "shift": "晚班", "personalShifts": 12, "totalShifts": 25, "personalRatio": 48, "historicalRatio": 60},
    {"name": "周四", "shift": "早班", "personalShifts": 20, "totalShifts": 30, "personalRatio": 66.7, "historicalRatio": 65},
    {"name": "吴五", "shift": "中班", "personalShifts": 16, "totalShifts": 18, "personalRatio": 88.9, "historicalRatio": 80},
]

# 岗位数据
positions_data = [
    {"positionId": "P001", "personalShifts": 20, "positionShifts": 45, "expectedRatio": 44.4, "month": "2026-04"},
    {"positionId": "P002", "personalShifts": 15, "positionShifts": 30, "expectedRatio": 50, "month": "2026-04"},
    {"positionId": "P003", "personalShifts": 18, "positionShifts": 40, "expectedRatio": 45, "month": "2026-04"},
    {"positionId": "P004", "personalShifts": 12, "positionShifts": 25, "expectedRatio": 48, "month": "2026-04"},
    {"positionId": "P005", "personalShifts": 22, "positionShifts": 50, "expectedRatio": 44, "month": "2026-04"},
]


def get_frontend_path():
    """
    获取前端文件路径
    支持打包后的exe和开发模式

    Returns:
        str: 前端目录路径
    """
    import sys
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的exe模式 - 单文件模式
        # 数据文件在临时目录中
        base_path = sys._MEIPASS
    else:
        # 开发环境模式
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, 'frontend')


@app.get('/')
async def index():
    """
    首页路由 - 提供前端页面
    """
    frontend_path = get_frontend_path()
    index_path = os.path.join(frontend_path, 'index.html')
    return FileResponse(index_path)


@app.get('/api/dashboard/stats', response_model=dict)
async def get_dashboard_stats():
    """
    获取仪表板统计数据
    """
    return {
        "totalEmployees": 50,
        "totalLeaves": len(leaves_data),
        "totalWorkHours": sum(item['hours'] for item in workhours_data),
        "totalShifts": sum(item['personalShifts'] for item in shifts_data)
    }


@app.get('/api/leaves', response_model=List[dict])
async def get_leaves(
    name: str = Query(None, description="按姓名筛选"),
    scheduled: str = Query(None, description="按排班状态筛选"),
    month: str = Query(None, description="按月份筛选")
):
    """
    获取请假数据列表
    支持按姓名、日期筛选
    """
    filtered_data = leaves_data.copy()

    # 按姓名筛选
    if name:
        filtered_data = [item for item in filtered_data if name.lower() in item['name'].lower()]

    # 按排班状态筛选
    if scheduled:
        filtered_data = [item for item in filtered_data if item['scheduled'] == scheduled]

    # 按月份筛选
    if month:
        filtered_data = [item for item in filtered_data if item['date'].startswith(month)]

    return filtered_data


@app.post('/api/leaves', status_code=201, response_model=dict)
async def create_leave(leave: LeaveCreate):
    """
    创建请假记录
    """
    # 添加新记录
    new_leave = {
        "name": leave.name,
        "date": leave.date,
        "scheduled": leave.scheduled
    }
    leaves_data.append(new_leave)

    return {"message": "请假记录创建成功", "data": new_leave}


@app.get('/api/workhours', response_model=List[dict])
async def get_workhours(
    search: str = Query(None, description="按姓名或ID搜索"),
    month: str = Query(None, description="按月份筛选")
):
    """
    获取工时数据列表
    支持按姓名、员工ID、月份筛选
    """
    filtered_data = workhours_data.copy()

    # 按姓名或ID筛选
    if search:
        filtered_data = [
            item for item in filtered_data
            if search.lower() in item['name'].lower() or search.lower() in item['id'].lower()
        ]

    # 按月份筛选
    if month:
        filtered_data = [item for item in filtered_data if item['month'] == month]

    return filtered_data


@app.post('/api/workhours', status_code=201, response_model=dict)
async def create_workhour(workhour: WorkHourCreate):
    """
    创建工时记录
    """
    # 添加新记录
    new_record = {
        "name": workhour.name,
        "id": workhour.id,
        "hours": workhour.hours,
        "month": workhour.month
    }
    workhours_data.append(new_record)

    return {"message": "工时记录创建成功", "data": new_record}


@app.get('/api/shifts', response_model=List[dict])
async def get_shifts(
    search: str = Query(None, description="按姓名搜索"),
    shiftType: str = Query(None, alias="shiftType", description="按班次类型筛选")
):
    """
    获取班次数据列表
    支持按姓名、班次类型筛选
    """
    filtered_data = shifts_data.copy()

    # 按姓名筛选
    if search:
        filtered_data = [item for item in filtered_data if search.lower() in item['name'].lower()]

    # 按班次类型筛选
    if shiftType:
        filtered_data = [item for item in filtered_data if item['shift'] == shiftType]

    return filtered_data


@app.post('/api/shifts', status_code=201, response_model=dict)
async def create_shift(shift: ShiftCreate):
    """
    创建班次记录
    """
    # 计算比例
    personal_ratio = (shift.personalShifts / shift.totalShifts * 100) if shift.totalShifts > 0 else 0

    # 添加新记录
    new_record = {
        "name": shift.name,
        "shift": shift.shift,
        "personalShifts": shift.personalShifts,
        "totalShifts": shift.totalShifts,
        "personalRatio": round(personal_ratio, 1),
        "historicalRatio": shift.historicalRatio if shift.historicalRatio is not None else personal_ratio
    }
    shifts_data.append(new_record)

    return {"message": "班次记录创建成功", "data": new_record}


@app.get('/api/positions', response_model=List[dict])
async def get_positions(
    search: str = Query(None, description="按岗位ID搜索"),
    month: str = Query(None, description="按月份筛选")
):
    """
    获取岗位工作数据列表
    支持按岗位ID、月份筛选
    """
    filtered_data = positions_data.copy()

    # 按岗位ID筛选
    if search:
        filtered_data = [item for item in filtered_data if search.lower() in item['positionId'].lower()]

    # 按月份筛选
    if month:
        filtered_data = [item for item in filtered_data if item['month'] == month]

    return filtered_data


@app.post('/api/positions', status_code=201, response_model=dict)
async def create_position(position: PositionCreate):
    """
    创建岗位工作记录
    """
    # 计算期望工作占比
    expected_ratio = (position.personalShifts / position.positionShifts * 100) if position.positionShifts > 0 else 0

    # 添加新记录
    new_record = {
        "positionId": position.positionId,
        "personalShifts": position.personalShifts,
        "positionShifts": position.positionShifts,
        "expectedRatio": round(expected_ratio, 1),
        "month": position.month if position.month else datetime.now().strftime('%Y-%m')
    }
    positions_data.append(new_record)

    return {"message": "岗位工作记录创建成功", "data": new_record}


@app.get('/{file_path:path}')
async def serve_static(file_path: str):
    """
    服务静态文件和页面
    支持SPA路由
    """
    frontend_path = get_frontend_path()

    # 如果是API请求，返回404
    if file_path.startswith('api/'):
        return JSONResponse(
            status_code=404,
            content={"error": "API endpoint not found"}
        )

    # 检查文件是否存在
    full_path = os.path.join(frontend_path, file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(full_path)

    # 如果文件不存在，返回index.html（SPA路由支持）
    index_path = os.path.join(frontend_path, 'index.html')
    return FileResponse(index_path)


if __name__ == '__main__':
    import uvicorn
    # 启动FastAPI开发服务器
    # 生产环境应使用Gunicorn或uvicorn
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=5000,
        reload=True
    )
