import platform

def print_environment_info():
    """打印环境信息"""
    print(f"检测环境: {platform.system()} {platform.release()} Python {platform.python_version()}")