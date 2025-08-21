from datetime import datetime

def generate_html(report_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Hikvision NVR 巡检报告</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            :root {{
                --primary-color: #2c3e50;
                --secondary-color: #3498db;
                --success-color: #2ecc71;
                --danger-color: #e74c3c;
                --warning-color: #f39c12;
                --light-bg: #f8f9fa;
                --abnormal-bg: #fff5f5;
                --card-shadow: 0 4px 12px rgba(0,0,0,0.08);
                --abnormal-shadow: 0 2px 8px rgba(231, 76, 60, 0.15);
                --transition-speed: 0.3s;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{ 
                font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; 
                background-color: var(--light-bg);
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            header {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: var(--card-shadow);
            }}
            
            h1 {{
                color: var(--primary-color);
                margin-bottom: 10px;
                font-weight: 600;
            }}
            
            .report-meta {{
                color: #666;
                font-size: 14px;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                flex-wrap: wrap;
            }}
            
            .status-badge {{
                display: inline-flex;
                align-items: center;
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 500;
            }}
            
            .status-online {{
                background-color: rgba(46, 204, 113, 0.15);
                color: var(--success-color);
            }}
            
            .status-offline {{
                background-color: rgba(231, 76, 60, 0.15);
                color: var(--danger-color);
            }}
            
            .status-recording {{
                background-color: rgba(46, 204, 113, 0.15);
                color: var(--success-color);
            }}
            
            .status-not-recording {{
                background-color: rgba(231, 76, 60, 0.15);
                color: var(--danger-color);
            }}
            
            .time-status-normal {{
                color: green;
                font-weight: bold;
            }}
            
            .time-status-abnormal {{
                color: red;
                font-weight: bold;
            }}
            
            .time-status-error {{
                color: orange;
                font-weight: bold;
            }}
            
            .nvr-card {{ 
                background-color: #fff; 
                border-radius: 10px; 
                box-shadow: var(--card-shadow); 
                margin: 0 0 25px 0; 
                overflow: hidden;
                transition: transform var(--transition-speed);
            }}
            
            .nvr-card:hover {{
                transform: translateY(-3px);
            }}
            
            .nvr-header {{ 
                cursor: pointer; 
                padding: 15px 20px; 
                font-size: 18px; 
                font-weight: 600; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                background-color: var(--primary-color); 
                color: white; 
            }}
            
            .nvr-header .nvr-info {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .nvr-header .nvr-stats {{
                display: flex;
                gap: 15px;
                font-size: 14px;
            }}
            
            .nvr-time-info {{
                padding: 10px 20px;
                background-color: #f0f7ff;
                border-bottom: 1px solid #e0e0e0;
                font-size: 14px;
                color: #333;
            }}
            
            .nvr-body {{
                padding: 20px;
            }}
            
            .channel-list {{ 
                display: none; 
                margin-top: 20px;
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 15px;
            }}
            
            .channel-card {{ 
                background-color: var(--light-bg); 
                padding: 15px; 
                border-radius: 8px; 
                border-left: 4px solid var(--secondary-color);
                transition: all var(--transition-speed);
            }}
            
            .channel-card.abnormal {{
                background-color: var(--abnormal-bg);
                border-left-color: var(--danger-color);
                box-shadow: var(--abnormal-shadow);
            }}
            
            .channel-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            }}
            
            .channel-card h4 {{
                margin-bottom: 10px;
                color: var(--primary-color);
                font-size: 16px;
                padding-bottom: 5px;
                border-bottom: 1px solid #eee;
            }}
            
            .channel-info {{
                font-size: 14px;
            }}
            
            .channel-info p {{
                margin-bottom: 6px;
                color: #555;
            }}
            
            .channel-info strong {{
                color: #333;
                width: 80px;
                display: inline-block;
            }}
            
            .toggle-icon {{
                transition: transform var(--transition-speed);
            }}
            
            .summary-stats {{
                display: flex;
                gap: 15px;
                margin: 0 0 30px 0;
                flex-wrap: wrap;
            }}
            
            .stat-card {{
                flex: 1;
                min-width: 180px;
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: var(--card-shadow);
                text-align: center;
            }}
            
            .stat-card .stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: var(--primary-color);
                margin: 5px 0;
            }}
            
            .stat-card .stat-label {{
                font-size: 14px;
                color: #666;
            }}
            
            @media (max-width: 768px) {{
                .channel-list {{
                    grid-template-columns: 1fr;
                }}
                
                .nvr-header {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 10px;
                }}
                
                .nvr-header .nvr-stats {{
                    width: 100%;
                    justify-content: space-between;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1><i class="fas fa-video"></i> Hikvision NVR 巡检报告</h1>
                <div class="report-meta">
                    <span><i class="far fa-calendar-alt"></i> 生成时间: {now}</span>
                    <span id="total-nvrs" class="status-badge"><i class="fas fa-server"></i> NVR总数: <span class="count">0</span></span>
                    <span id="online-nvrs" class="status-badge status-online"><i class="fas fa-check"></i> 在线NVR: <span class="count">0</span></span>
                    <span id="offline-nvrs" class="status-badge status-offline"><i class="fas fa-times"></i> 离线NVR: <span class="count">0</span></span>
                    <span id="total-channels" class="status-badge"><i class="fas fa-tv"></i> 总通道数: <span class="count">0</span></span>
                </div>
            </header>
            
            <div class="summary-stats">
                <div class="stat-card">
                    <i class="fas fa-eye" style="color: var(--secondary-color); font-size: 20px;"></i>
                    <div class="stat-value" id="online-channels">0</div>
                    <div class="stat-label">在线通道</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-eye-slash" style="color: var(--danger-color); font-size: 20px;"></i>
                    <div class="stat-value" id="offline-channels">0</div>
                    <div class="stat-label">离线通道</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-video" style="color: var(--success-color); font-size: 20px;"></i>
                    <div class="stat-value" id="recording-channels">0</div>
                    <div class="stat-label">正常录制</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-video-slash" style="color: var(--warning-color); font-size: 20px;"></i>
                    <div class="stat-value" id="not-recording-channels">0</div>
                    <div class="stat-label">录制异常</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-clock" style="color: #9b59b6; font-size: 20px;"></i>
                    <div class="stat-value" id="time-normal-count">0</div>
                    <div class="stat-label">时间正常</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-clock" style="color: var(--danger-color); font-size: 20px;"></i>
                    <div class="stat-value" id="time-abnormal-count">0</div>
                    <div class="stat-label">时间异常</div>
                </div>
            </div>
    """

    for nvr_name, data in report_data.items():
        nvr_online = data['online']
        channels = data['channels']
        time_info = data['time_info']
        
        time_status_class = "time-status-normal" if time_info['time_status'] == "正常" else \
                           "time-status-abnormal" if time_info['time_status'] == "异常" else "time-status-error"
        
        nvr_status = f"<span class='status-badge status-online'><i class='fas fa-check'></i> 在线</span>" if nvr_online else f"<span class='status-badge status-offline'><i class='fas fa-times'></i> 离线</span>"
        
        online_ch = sum(1 for ch in channels if ch['online'])
        offline_ch = len(channels) - online_ch
        recording_ch = sum(1 for ch in channels if ch['enableTiming'] == 'true')
        not_recording_ch = len(channels) - recording_ch

        html += f"""
        <div class="nvr-card">
            <div class="nvr-header" onclick="toggleVisibility(this)">
                <div class="nvr-info">
                    <i class="fas fa-server"></i>
                    <span>{nvr_name}</span>
                </div>
                <div class="nvr-stats">
                    {nvr_status}
                    <span>通道总数: {len(channels)}</span>
                    <span>在线: {online_ch}</span>
                    <span>离线: {offline_ch}</span>
                    <span class="toggle-icon"><i class="fas fa-chevron-down"></i></span>
                </div>
            </div>
            
            <div class="nvr-time-info">
                <i class="fas fa-clock"></i> 
                设备时间: {time_info['device_time']} | 
                本机时间: {time_info['local_time']} | 
                时间差: {time_info['time_diff']}秒 | 
                状态: <span class="{time_status_class}">{time_info['time_status']}</span>
            </div>
            
            <div class="nvr-body">
                <div class="channel-list" style="display: none;">
        """

        if channels:
            for ch in channels:
                ch_status = f"<span class='status-badge status-online'><i class='fas fa-check'></i> 在线</span>" if ch['online'] else f"<span class='status-badge status-offline'><i class='fas fa-times'></i> 离线</span>"
                record_status = f"<span class='status-badge status-recording'><i class='fas fa-video'></i> 正常</span>" if ch['enableTiming'] == 'true' else f"<span class='status-badge status-not-recording'><i class='fas fa-exclamation-triangle'></i> 异常</span>"
                
                is_abnormal = not ch['online'] or ch['enableTiming'] == 'false'
                abnormal_class = "abnormal" if is_abnormal else ""

                display_model = ch['model'] if ch['model'] is not None else '<span style="color: #e74c3c;">未获取</span>'
                display_serial = ch['serialNumber'] if ch['serialNumber'] is not None else '<span style="color: #e74c3c;">未获取</span>'

                html += f"""
                <div class="channel-card {abnormal_class}">
                    <h4>通道 {ch['id']}: {ch['name']}</h4>
                    <div class="channel-info">
                        <p><strong>IP地址:</strong> {ch['ip'] or '未知'}</p>
                        <p><strong>型号:</strong> {display_model}</p>
                        <p><strong>序列号:</strong> {display_serial}</p>
                        <p><strong>状态:</strong> {ch_status}</p>
                        <p><strong>录制:</strong> {record_status}</p>
                    </div>
                </div>
                """
        else:
            html += """
            <div style="grid-column: 1 / -1; text-align: center; padding: 20px; color: #666;">
                <i class="fas fa-info-circle" style="font-size: 24px; margin-bottom: 10px; color: var(--warning-color);"></i>
                <p>没有获取到通道信息</p>
            </div>
            """

        html += "</div></div></div>"

    html += """
    </div>
    <script>
        function toggleVisibility(header) {
            const list = header.nextElementSibling.nextElementSibling.querySelector('.channel-list');
            const icon = header.querySelector('.toggle-icon i');
            
            if (list.style.display === "none" || list.style.display === "") {
                list.style.display = "grid";
                icon.classList.add('fa-chevron-up');
                icon.classList.remove('fa-chevron-down');
            } else {
                list.style.display = "none";
                icon.classList.add('fa-chevron-down');
                icon.classList.remove('fa-chevron-up');
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            const nvrCards = document.querySelectorAll('.nvr-card');
            const totalNvrs = nvrCards.length;
            let onlineNvrs = 0;
            let timeNormalCount = 0;
            let timeAbnormalCount = 0;
            
            let totalChannels = 0;
            let onlineChannels = 0;
            let offlineChannels = 0;
            let recordingChannels = 0;
            let notRecordingChannels = 0;
            
            nvrCards.forEach(card => {
                const header = card.querySelector('.nvr-header');
                if (header.innerHTML.includes('status-online')) {
                    onlineNvrs++;
                }
                
                const timeStatusEl = card.querySelector('.nvr-time-info span');
                if (timeStatusEl.classList.contains('time-status-normal')) {
                    timeNormalCount++;
                } else if (timeStatusEl.classList.contains('time-status-abnormal')) {
                    timeAbnormalCount++;
                }
                
                const channelCards = card.querySelectorAll('.channel-card');
                totalChannels += channelCards.length;
                
                channelCards.forEach(channel => {
                    if (channel.innerHTML.includes('status-online')) {
                        onlineChannels++;
                    } else {
                        offlineChannels++;
                    }
                    
                    if (channel.innerHTML.includes('status-recording')) {
                        recordingChannels++;
                    } else {
                        notRecordingChannels++;
                    }
                });
            });
            
            document.getElementById('total-nvrs').querySelector('.count').textContent = totalNvrs;
            document.getElementById('online-nvrs').querySelector('.count').textContent = onlineNvrs;
            document.getElementById('offline-nvrs').querySelector('.count').textContent = totalNvrs - onlineNvrs;
            document.getElementById('total-channels').querySelector('.count').textContent = totalChannels;
            
            document.getElementById('online-channels').textContent = onlineChannels;
            document.getElementById('offline-channels').textContent = offlineChannels;
            document.getElementById('recording-channels').textContent = recordingChannels;
            document.getElementById('not-recording-channels').textContent = notRecordingChannels;
            document.getElementById('time-normal-count').textContent = timeNormalCount;
            document.getElementById('time-abnormal-count').textContent = timeAbnormalCount;
        });
    </script>
    </body>
    </html>
    """

    with open("nvr_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML报告已生成: nvr_report.html")
    return "nvr_report.html"