"""
拜耳制药排班系统 - 启动脚本
用于打包成Windows可执行文件

该脚本负责：
1. 获取程序所在目录
2. 配置Flask应用
3. 启动Web服务器
4. 自动打开浏览器
"""

import os
import sys
import webbrowser
from threading import Timer


def get_application_path():
    """
    获取应用程序所在目录
    支持打包后的exe和直接运行Python脚本两种模式

    Returns:
        str: 应用程序根目录路径
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的exe模式
        return os.path.dirname(sys.executable)
    else:
        # 开发环境直接运行Python脚本模式
        return os.path.dirname(os.path.abspath(__file__))


def open_browser_tab(url, delay=1.5):
    """
    延迟打开浏览器标签页
    给予Flask服务器足够的启动时间

    Args:
        url (str): 要打开的URL地址
        delay (float): 延迟时间（秒）
    """
    def _open():
        webbrowser.open(url)
    Timer(delay, _open).start()


def main():
    """
    主函数 - 启动Flask应用
    """
    # 获取应用根目录
    app_root = get_application_path()

    print("=" * 60)
    print("  拜耳制药排班系统 - 数据分析平台")
    print("=" * 60)
    print(f"\n应用目录: {app_root}")
    print("\n正在启动服务器...")

    try:
        # 导入Flask应用
        from backend.app import app

        # 配置静态文件和模板路径
        # 前端文件位于 app_root/frontend/
        frontend_path = os.path.join(app_root, 'frontend')

        if not os.path.exists(frontend_path):
            print(f"\n错误: 找不到前端文件目录: {frontend_path}")
            print("请确保frontend文件夹存在于应用程序所在目录。")
            input("\n按Enter键退出...")
            sys.exit(1)

        # 设置Flask配置
        app.config['FRONTEND_PATH'] = frontend_path
        app.config['HOST'] = '127.0.0.1'
        app.config['PORT'] = 5000

        # 定义路由来服务前端文件
        @app.route('/')
        def serve_index():
            """服务主页"""
            from flask import send_from_directory
            return send_from_directory(frontend_path, 'index.html')

        @app.route('/<path:filename>')
        def serve_static(filename):
            """服务静态文件"""
            from flask import send_from_directory
            # 检查文件是否在pages目录下
            if filename.startswith('pages/'):
                return send_from_directory(frontend_path, filename)
            # 其他静态文件
            return send_from_directory(frontend_path, filename)

        # 启动URL
        server_url = f"http://127.0.0.1:5000/"

        print(f"\n✓ 服务器启动成功！")
        print(f"✓ 访问地址: {server_url}")
        print(f"\n将在浏览器中自动打开应用...")
        print(f"\n按 Ctrl+C 或关闭此窗口停止服务器。")
        print("=" * 60)

        # 延迟打开浏览器，给予服务器启动时间
        open_browser_tab(server_url, delay=1.5)

        # 启动Flask开发服务器
        # 使用threaded=True支持多线程并发请求
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,           # 打包后关闭debug模式
            threaded=True,
            use_reloader=False    # 打包后关闭自动重载
        )

    except ImportError as e:
        print(f"\n错误: 导入模块失败 - {e}")
        print("\n请确保已安装所有依赖：")
        print("  pip install -r backend/requirements.txt")
        input("\n按Enter键退出...")
        sys.exit(1)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按Enter键退出...")
        sys.exit(1)


if __name__ == '__main__':
    main()
