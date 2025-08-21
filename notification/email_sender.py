import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import socket
from datetime import datetime
from config.settings import EMAIL_CONFIG, NVR_LIST

def send_email(report_data, report_file_path):
    """按指定格式发送邮件，异常用红色🔴，正常用绿色🟢"""
    try:
        if EMAIL_CONFIG["smtp_server"] in ["smtp.example.com", ""]:
            print("请配置正确的邮件服务器信息以发送邮件")
            return False
            
        print(f"开始发送邮件，服务器: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        
        # 构建邮件内容
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG["sender"]
        msg['To'] = ", ".join(EMAIL_CONFIG["receivers"])
        msg['Subject'] = EMAIL_CONFIG["subject"]
        
        # 构建邮件正文（按要求格式）
        body = "海康威视设备巡检结果：\n\n"
        
        # 遍历所有NVR设备
        for nvr_name, data in report_data.items():
            # 获取NVR的IP地址
            nvr_ip = next(nvr['ip'] for nvr in NVR_LIST if nvr['name'] == nvr_name)
            nvr_online = data['online']
            channels = data['channels']
            time_info = data['time_info']
            
            # 检查是否有异常（设备离线、通道离线、时间异常）
            offline_channels = [ch for ch in channels if not ch['online']]
            time_abnormal = time_info['time_status'] != "正常"
            has_abnormal = not nvr_online or len(offline_channels) > 0 or time_abnormal
            
            # 异常用🔴，正常用🟢
            status_icon = "🔴" if has_abnormal else "🟢"
            
            # 设备离线情况
            if not nvr_online:
                body += f"{status_icon} {nvr_name}({nvr_ip}) 设备离线，请优先检查设备连接！\n"
                continue  # 设备离线无需检查通道
            
            # 收集异常详情
            abnormal_details = []
            if time_abnormal:
                abnormal_details.append(f"时间同步异常（差值: {time_info['time_diff']}秒）")
            
            if len(offline_channels) > 0:
                # 格式化离线通道信息
                channel_desc = ", ".join([f"{ch['name']}(IP:{ch['ip'] or '未知'})" for ch in offline_channels])
                abnormal_details.append(f"有以下通道离线，请及时检查：\n   {channel_desc}")
            
            # 生成设备状态行
            if has_abnormal:
                body += f"{status_icon} {nvr_name}({nvr_ip}) "
                body += "\n   ".join(abnormal_details) + "\n"
            else:
                body += f"{status_icon} {nvr_name}({nvr_ip}) 所有通道均正常，时间同步正常\n"
        
        # 添加报告生成时间
        body += f"\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 添加附件
        try:
            with open(report_file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {report_file_path}",
            )
            msg.attach(part)
            print(f"成功添加附件: {report_file_path}")
        except Exception as e:
            print(f"添加附件失败: {str(e)}")
            return False
        
        # 发送邮件（适配Python 3.7的超时处理）
        server = None
        try:
            # 设置全局超时
            socket.setdefaulttimeout(EMAIL_CONFIG["timeout"])
            
            # 根据端口选择连接方式（465通常用SSL）
            if EMAIL_CONFIG["smtp_port"] == 465:
                server = smtplib.SMTP_SSL(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
                print("使用SSL连接邮件服务器")
            else:
                server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
                print("使用普通连接，尝试启用TLS")
                server.starttls()  # 启用TLS加密
            
            # 登录并发送
            server.login(EMAIL_CONFIG["smtp_username"], EMAIL_CONFIG["smtp_password"])
            print("成功登录邮件服务器")
            
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG["sender"], EMAIL_CONFIG["receivers"], text)
            print("邮件发送成功！")
            return True
            
        except socket.timeout:
            print(f"邮件服务器连接超时（{EMAIL_CONFIG['timeout']}秒）")
            return False
        except smtplib.SMTPAuthenticationError:
            print("邮件服务器认证失败，请检查用户名和授权码是否正确")
            return False
        except Exception as e:
            print(f"邮件发送过程中出错: {str(e)}")
            return False
        finally:
            if server:
                try:
                    server.quit()
                    print("已关闭邮件服务器连接")
                except:
                    pass
                    
    except Exception as e:
        print(f"邮件发送准备过程中出错: {str(e)}")
        return False