import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
from datetime import datetime
from config.settings import ENABLE_DEBUG
from .time_checker import get_device_time 

def fetch_channels(nvr):
    url = f"http://{nvr['ip']}/ISAPI/ContentMgmt/InputProxy/channels"
    try:
        response = requests.get(url, auth=HTTPDigestAuth(nvr['username'], nvr['password']), timeout=5)
        response.raise_for_status()
        nvr_online = True
    except requests.RequestException as e:
        print(f"[{nvr['name']}] 请求失败: {e}")
        # 当NVR无法连接时，仍尝试获取时间信息
        time_info = get_device_time(nvr)  # 这里调用 get_device_time
        return [], False, time_info

    time_info = get_device_time(nvr)  # 这里也调用 get_device_time
    
    ns = {'hik': 'http://www.hikvision.com/ver20/XMLSchema'}
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"[{nvr['name']}] 解析 XML 失败: {e}")
        return [], nvr_online, time_info

    channels = []
    for ch in root.findall('hik:InputProxyChannel', ns):
        id_ = ch.find('hik:id', ns).text
        name = ch.find('hik:name', ns).text
        src = ch.find('hik:sourceInputPortDescriptor', ns)
        
        ip = src.find('hik:ipAddress', ns).text if src.find('hik:ipAddress', ns) is not None else ''
        model = src.find('hik:model', ns).text if src.find('hik:model', ns) is not None else ''
        serial = src.find('hik:serialNumber', ns).text if src.find('hik:serialNumber', ns) is not None else ''
        enableTiming = ch.find('hik:enableTiming', ns).text if ch.find('hik:enableTiming', ns) is not None else 'false'
        
        model_str = str(model) if model is not None else ''
        serial_str = str(serial) if serial is not None else ''
        model_valid = bool(model_str.strip())
        serial_valid = bool(serial_str.strip())
        online = model_valid and serial_valid
        
        if ENABLE_DEBUG:
            print(f"通道 {id_} 判断: 型号={'有效' if model_valid else '无效'}, 序列号={'有效' if serial_valid else '无效'}, 在线状态={online}")
        
        channels.append({
            "id": id_,
            "name": name,
            "ip": ip,
            "model": model,
            "serialNumber": serial,
            "enableTiming": enableTiming,
            "online": online
        })
    
    return channels, nvr_online, time_info