@echo off
echo 🚀 啟動員工學習效率分析伺服器...
echo.
echo 📱 本機網址: http://localhost:8501
echo 🌐 網路網址: http://%COMPUTERNAME%:8501
echo.
echo ⏹️  按 Ctrl+C 停止伺服器
echo ----------------------------------------
echo.

python -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true

pause
