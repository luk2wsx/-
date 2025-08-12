#!/bin/bash

echo "🚀 啟動員工學習效率分析伺服器..."
echo ""
echo "📱 本機網址: http://localhost:8501"
echo "🌐 網路網址: http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "⏹️  按 Ctrl+C 停止伺服器"
echo "----------------------------------------"
echo ""

python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
