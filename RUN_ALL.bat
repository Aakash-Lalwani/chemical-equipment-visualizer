@echo off
cls
echo.
echo ============================================================
echo  CHEMICAL EQUIPMENT PARAMETER VISUALIZER
echo  Complete Project Launcher
echo ============================================================
echo.
echo Starting all components...
echo.

REM Start Backend in new window
echo [1/3] Starting Django Backend...
start "BACKEND - Django Server" cmd /k "cd /d c:\Users\91985\Desktop\FOSSE_2026\backend && c:\Users\91985\Desktop\FOSSE_2026\.venv\Scripts\python.exe manage.py runserver"
timeout /t 3 /nobreak >nul

REM Start Frontend in new window (if Node.js is installed)
echo [2/3] Starting React Frontend...
where node >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "FRONTEND - React Dev Server" cmd /k "cd /d c:\Users\91985\Desktop\FOSSE_2026\frontend-react && npm run dev"
) else (
    echo Node.js not found - Frontend skipped
    echo Install Node.js from: https://nodejs.org/
)
timeout /t 2 /nobreak >nul

REM Start Desktop App in new window
echo [3/3] Starting Desktop Application...
start "DESKTOP - PyQt5 App" cmd /k "cd /d c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt && c:\Users\91985\Desktop\FOSSE_2026\.venv\Scripts\python.exe main.py"
timeout /t 2 /nobreak >nul

echo.
echo ============================================================
echo  ALL COMPONENTS STARTED!
echo ============================================================
echo.
echo  BACKEND:  http://127.0.0.1:8000
echo  FRONTEND: http://localhost:3000  (if Node.js installed)
echo  DESKTOP:  Window opened
echo.
echo  Credentials: admin / admin123
echo.
echo ============================================================
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

REM Try to open browser
where node >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start http://localhost:3000
) else (
    start http://127.0.0.1:8000/admin
)

echo.
echo Keep the terminal windows open!
echo Close them to stop the servers.
echo.
pause
