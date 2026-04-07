@echo off
echo Starting Dalal Street Talkies Platform...

:: Start the Main Flask Website Backend on default port 5000
echo Launching Core Flask App...
start "Flask Frontend" python app.py

:: Delay slightly to stagger initializations
timeout /t 2 /nobreak >nul

:: Start Stock Prediction Model explicitly on Port 8501
echo Launching Stock Prediction Server (Port 8501)...
start "Streamlit - Stocks" streamlit run lstm.py --server.port 8501

:: Start Mutual Funds Analytics explicitly on Port 8502
echo Launching Mutual Funds Server (Port 8502)...
start "Streamlit - Funds" streamlit run mutualfunds.py --server.port 8502

:: Start AI Chatbot explicitly on Port 8503
echo Launching Pulse AI Server (Port 8503)...
start "Streamlit - AI" streamlit run chat.py --server.port 8503

echo All systems are launching!
echo.
echo ==============================================
echo [1] Master Dashboard: http://127.0.0.1:5000
echo [2] Predict Stocks:   http://localhost:8501
echo [3] Mutual Funds:     http://localhost:8502
echo [4] Pulse AI Chatbot: http://localhost:8503
echo ==============================================
echo.
pause
