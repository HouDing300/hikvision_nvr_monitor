import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
from datetime import datetime
from config.settings import TIME_THRESHOLD, ENABLE_DEBUG

def get_device_time(nvr):
    """获取设备时间并与本机时间对比"""
    url = f"http://{nvr['ip']}/ISAPI/System/time"
    try:
        response = requests.get(
            url, 
            auth=HTTPDigestAuth(nvr['username'], nvr['password']), 
            timeout=10
        )
        response.raise_for_status()
        
        ns = {'hik': 'http://www.hikvision.com/ver20/XMLSchema'}
        root = ET.fromstring(response.content)
        
        local_time_elem = root.find('hik:localTime', ns)
        if local_time_elem is None:
            raise ValueError("未找到localTime字段")
            
        device_time_str = local_time_elem.text
        if not device_time_str:
            raise ValueError("localTime字段为空")
        
        if '+' in device_time_str:
            device_time_str = device_time_str.split('+')[0]
        device_time = datetime.strptime(device_time_str, "%Y-%m-%dT%H:%M:%S")
        
        local_time = datetime.now()
        time_diff = abs((device_time - local_time).total_seconds())
        
        time_status = "正常" if time_diff <= TIME_THRESHOLD else "异常"
        time_status_color = "green" if time_diff <= TIME_THRESHOLD else "red"
        
        if ENABLE_DEBUG:
            print(f"[{nvr['name']}] 设备时间: {device_time}, 本机时间: {local_time}, 差值: {time_diff:.2f}秒, 状态: {time_status}")
            
        return {
            "device_time": device_time_str,
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "time_diff": f"{time_diff:.2f}",
            "time_status": time_status,
            "time_status_color": time_status_color,
            "success": True
        }
        
    except Exception as e:
        print(f"[{nvr['name']}] 获取时间失败: {str(e)}")
        return {
            "device_time": "获取失败",
            "local_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time_diff": "N/A",
            "time_status": "异常",  # 获取失败视为时间异常
            "time_status_color": "orange",
            "success": False
        }