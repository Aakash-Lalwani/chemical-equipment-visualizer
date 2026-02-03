@echo off
cls
echo.
echo ============================================================
echo  DEMO VIDEO SETUP
echo  Chemical Equipment Parameter Visualizer
echo ============================================================
echo.
echo This script will prepare your project for demo recording...
echo.

cd /d "%~dp0"

REM Step 1: Database check
echo [1/4] Checking database...
cd backend
.venv\Scripts\python.exe manage.py migrate --run-syncdb >nul 2>&1
echo     Database ready!

REM Step 2: Ensure admin user exists
echo [2/4] Setting up demo user...
.venv\Scripts\python.exe -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@demo.com', 'admin123'); print('Admin user ready!')"

REM Step 3: Clear old terminals
echo [3/4] Clearing old processes...
taskkill /F /FI "WINDOWTITLE eq BACKEND*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq FRONTEND*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq DESKTOP*" >nul 2>&1
timeout /t 2 /nobreak >nul

REM Step 4: Start fresh
echo [4/4] Starting all components...
cd ..
call RUN_ALL.bat

echo.
echo ============================================================
echo  DEMO ENVIRONMENT READY!
echo ============================================================
echo.
echo  Backend:  http://127.0.0.1:8000
echo  Frontend: http://localhost:5173
echo  Desktop:  Login window open
echo.
echo  Login with: admin / admin123
echo.
echo ============================================================
