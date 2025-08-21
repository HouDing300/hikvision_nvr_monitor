from config.settings import NVR_LIST
from core.nvr_api import fetch_channels
from reporting.json_handler import save_to_json
from reporting.html_generator import generate_html
from notification.email_sender import send_email
from utils.helpers import print_environment_info
import platform
from datetime import datetime  # 添加这行

def main():
    print_environment_info()
    all_data = {}
    for nvr in NVR_LIST:
        print(f"\n正在获取 NVR: {nvr['name']} ({nvr['ip']})")
        channels, nvr_online, time_info = fetch_channels(nvr)
        
        # 确保time_info始终有值
        if time_info is None:
            time_info = {
                "device_time": "获取失败",
                "local_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "time_diff": "N/A",
                "time_status": "异常",
                "time_status_color": "orange",
                "success": False
            }
            
        all_data[nvr['name']] = {
            "online": nvr_online,
            "channels": channels,
            "time_info": time_info
        }
        online_count = sum(1 for ch in channels if ch['online'])
        print(f"[{nvr['name']}] 共找到 {len(channels)} 个通道，其中 {online_count} 个在线")
        print(f"[{nvr['name']}] 时间状态: {time_info['time_status']} (差值: {time_info['time_diff']}秒)")

    # 保存 JSON
    save_to_json(all_data)

    # 生成 HTML 报告（本地生成）
    report_file = generate_html(all_data)
    
    # 发送邮件
    print("开始处理邮件发送...")
    email_success = send_email(all_data, report_file)
    if not email_success:
        print("邮件发送失败，请检查配置和网络")
    
    print("程序执行完毕")

if __name__ == "__main__":
    main()