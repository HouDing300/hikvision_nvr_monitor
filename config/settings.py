# ================== 配置项 ==================
NVR_LIST = [
    {"name": "NVR1", "ip": "1.1.1.1", "username": "admin", "password": "1111111"},
    {"name": "NVR2", "ip": "2.2.2.2", "username": "admin", "password": "1111111"},
    # 可以继续添加更多 NVR
]

# 邮件配置 - 请根据实际情况修改
EMAIL_CONFIG = {
    "smtp_server": "***.***.***",      # 邮箱SMTP服务器
    "smtp_port": 465,                   # 邮箱SSL端口(推荐)
    "smtp_username": "11111",           # 替换为你的邮箱
    "smtp_password": "1111111",         # 替换为邮箱授权码(非登录密码)
    "sender": "1111111111",             # 发件人邮箱
    "receivers": ["111111111.com"],     # 收件人列表
    "subject": "海康威视设备巡检报告",    # 优化邮件主题
    "timeout": 15                       # 邮件服务器连接超时时间(秒)
}

# 时间对比阈值(秒)
TIME_THRESHOLD = 30

# 调试信息开关
ENABLE_DEBUG = True