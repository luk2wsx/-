#!/usr/bin/env python3
"""
員工學習效率分析 - 伺服器啟動檔案
"""

import subprocess
import sys
import os
import socket

def get_local_ip():
    """取得本機 IP 地址"""
    try:
        # 連接到外部地址來取得本機 IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """啟動 Streamlit 伺服器"""
    port = 8501
    local_ip = get_local_ip()
    
    print("🚀 啟動員工學習效率分析伺服器...")
    print(f"📱 本機網址: http://localhost:{port}")
    print(f"🌐 網路網址: http://{local_ip}:{port}")
    print("⏹️  按 Ctrl+C 停止伺服器")
    print("-" * 50)
    
    try:
        # 啟動 Streamlit 伺服器
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'app.py', 
            '--server.port', str(port),
            '--server.address', '0.0.0.0',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n🛑 伺服器已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

if __name__ == '__main__':
    main()
