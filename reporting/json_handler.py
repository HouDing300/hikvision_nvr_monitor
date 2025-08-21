import json

def save_to_json(data, filename="nvr_channels.json"):
    """保存数据到JSON文件"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到: {filename}")
    return filename