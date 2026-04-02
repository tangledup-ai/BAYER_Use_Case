"""
拜耳制药排班系统 - 后端API服务
使用Flask框架提供RESTful API接口
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

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


@app.route('/')
def index():
    """
    首页路由
    """
    return jsonify({
        "message": "拜耳制药排班系统 API 服务",
        "version": "1.0.0",
        "status": "running"
    })


@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """
    获取仪表板统计数据
    """
    return jsonify({
        "totalEmployees": 50,
        "totalLeaves": len(leaves_data),
        "totalWorkHours": sum(item['hours'] for item in workhours_data),
        "totalShifts": sum(item['personalShifts'] for item in shifts_data)
    })


@app.route('/api/leaves', methods=['GET'])
def get_leaves():
    """
    获取请假数据列表
    支持按姓名、日期筛选
    """
    search_name = request.args.get('name', '').lower()
    scheduled = request.args.get('scheduled', '')
    month = request.args.get('month', '')

    filtered_data = leaves_data.copy()

    # 按姓名筛选
    if search_name:
        filtered_data = [item for item in filtered_data if search_name in item['name'].lower()]

    # 按排班状态筛选
    if scheduled:
        filtered_data = [item for item in filtered_data if item['scheduled'] == scheduled]

    # 按月份筛选
    if month:
        filtered_data = [item for item in filtered_data if item['date'].startswith(month)]

    return jsonify(filtered_data)


@app.route('/api/leaves', methods=['POST'])
def create_leave():
    """
    创建请假记录
    """
    data = request.get_json()

    # 数据验证
    required_fields = ['name', 'date', 'scheduled']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"缺少必填字段: {field}"}), 400

    # 添加新记录
    new_leave = {
        "name": data['name'],
        "date": data['date'],
        "scheduled": data['scheduled']
    }
    leaves_data.append(new_leave)

    return jsonify({"message": "请假记录创建成功", "data": new_leave}), 201


@app.route('/api/workhours', methods=['GET'])
def get_workhours():
    """
    获取工时数据列表
    支持按姓名、员工ID、月份筛选
    """
    search = request.args.get('search', '').lower()
    month = request.args.get('month', '')

    filtered_data = workhours_data.copy()

    # 按姓名或ID筛选
    if search:
        filtered_data = [
            item for item in filtered_data
            if search in item['name'].lower() or search in item['id'].lower()
        ]

    # 按月份筛选
    if month:
        filtered_data = [item for item in filtered_data if item['month'] == month]

    return jsonify(filtered_data)


@app.route('/api/workhours', methods=['POST'])
def create_workhour():
    """
    创建工时记录
    """
    data = request.get_json()

    # 数据验证
    required_fields = ['name', 'id', 'hours', 'month']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"缺少必填字段: {field}"}), 400

    # 添加新记录
    new_record = {
        "name": data['name'],
        "id": data['id'],
        "hours": data['hours'],
        "month": data['month']
    }
    workhours_data.append(new_record)

    return jsonify({"message": "工时记录创建成功", "data": new_record}), 201


@app.route('/api/shifts', methods=['GET'])
def get_shifts():
    """
    获取班次数据列表
    支持按姓名、班次类型筛选
    """
    search = request.args.get('search', '').lower()
    shift_type = request.args.get('shiftType', '')

    filtered_data = shifts_data.copy()

    # 按姓名筛选
    if search:
        filtered_data = [item for item in filtered_data if search in item['name'].lower()]

    # 按班次类型筛选
    if shift_type:
        filtered_data = [item for item in filtered_data if item['shift'] == shift_type]

    return jsonify(filtered_data)


@app.route('/api/shifts', methods=['POST'])
def create_shift():
    """
    创建班次记录
    """
    data = request.get_json()

    # 数据验证
    required_fields = ['name', 'shift', 'personalShifts', 'totalShifts']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"缺少必填字段: {field}"}), 400

    # 计算比例
    personal_ratio = (data['personalShifts'] / data['totalShifts'] * 100) if data['totalShifts'] > 0 else 0

    # 添加新记录
    new_record = {
        "name": data['name'],
        "shift": data['shift'],
        "personalShifts": data['personalShifts'],
        "totalShifts": data['totalShifts'],
        "personalRatio": round(personal_ratio, 1),
        "historicalRatio": data.get('historicalRatio', personal_ratio)
    }
    shifts_data.append(new_record)

    return jsonify({"message": "班次记录创建成功", "data": new_record}), 201


@app.route('/api/positions', methods=['GET'])
def get_positions():
    """
    获取岗位工作数据列表
    支持按岗位ID、月份筛选
    """
    search = request.args.get('search', '').lower()
    month = request.args.get('month', '')

    filtered_data = positions_data.copy()

    # 按岗位ID筛选
    if search:
        filtered_data = [item for item in filtered_data if search in item['positionId'].lower()]

    # 按月份筛选
    if month:
        filtered_data = [item for item in filtered_data if item['month'] == month]

    return jsonify(filtered_data)


@app.route('/api/positions', methods=['POST'])
def create_position():
    """
    创建岗位工作记录
    """
    data = request.get_json()

    # 数据验证
    required_fields = ['positionId', 'personalShifts', 'positionShifts']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"缺少必填字段: {field}"}), 400

    # 计算期望工作占比
    expected_ratio = (data['personalShifts'] / data['positionShifts'] * 100) if data['positionShifts'] > 0 else 0

    # 添加新记录
    new_record = {
        "positionId": data['positionId'],
        "personalShifts": data['personalShifts'],
        "positionShifts": data['positionShifts'],
        "expectedRatio": round(expected_ratio, 1),
        "month": data.get('month', datetime.now().strftime('%Y-%m'))
    }
    positions_data.append(new_record)

    return jsonify({"message": "岗位工作记录创建成功", "data": new_record}), 201


@app.errorhandler(404)
def not_found(error):
    """
    404错误处理
    """
    return jsonify({"error": "资源未找到"}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    500错误处理
    """
    return jsonify({"error": "服务器内部错误"}), 500


if __name__ == '__main__':
    # 启动Flask开发服务器
    # 生产环境应使用Gunicorn或uWSGI
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
