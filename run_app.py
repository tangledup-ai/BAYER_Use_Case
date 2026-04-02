"""
拜耳制药排班系统 - 启动脚本
用于打包成Windows可执行文件

该脚本负责：
1. 获取程序所在目录
2. 启动FastAPI应用服务器
3. 自动打开浏览器
"""

import os
import sys
import webbrowser
from threading import Timer
import uvicorn

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
    给予FastAPI服务器足够的启动时间

    Args:
        url (str): 要打开的URL地址
        delay (float): 延迟时间（秒）
    """
    def _open():
        webbrowser.open(url)
    Timer(delay, _open).start()


def main():
    """
    主函数 - 启动FastAPI应用
    """
    # 获取应用根目录
    app_root = get_application_path()

    print("=" * 60)
    print("  拜耳制药排班系统 - 数据分析平台")
    print("=" * 60)
    print(f"\n应用目录: {app_root}")
    print("\n正在启动服务器...")

    try:
        # 导入FastAPI应用
        from backend.app import app

        # 检查前端文件是否存在
        frontend_path = os.path.join(app_root, 'frontend')
        if not os.path.exists(frontend_path):
            print(f"\n警告: 找不到前端文件目录: {frontend_path}")
            print("请确保frontend文件夹存在于应用程序所在目录。")

        # 启动URL
        server_url = "http://127.0.0.1:5000/"

        print(f"\n[OK] 服务器启动成功!")
        print(f"[OK] 访问地址: {server_url}")
        print(f"[OK] API文档地址: {server_url}docs")
        print(f"\n将在浏览器中自动打开应用...")
        print(f"\n按 Ctrl+C 或关闭此窗口停止服务器。")
        print("=" * 60)

        # 延迟打开浏览器，给予服务器启动时间
        open_browser_tab(server_url, delay=1.5)

        # 启动uvicorn服务器
        uvicorn.run(
            app,
            host='127.0.0.1',
            port=5000,
            log_level="info",
            use_colors=True
        )

    except ImportError as e:
        print(f"\n错误: 导入模块失败 - {e}")
        print("\n请确保已安装所有依赖：")
        print("  pip install -r requirements.txt")
        print("\n按任意键退出...")
        if sys.stdout.isatty():
            input()
        else:
            import time
            time.sleep(3)
        sys.exit(1)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        print("\n按任意键退出...")
        if sys.stdout.isatty():
            input()
        else:
            import time
            time.sleep(5)
        sys.exit(1)


if __name__ == '__main__':
    main()
