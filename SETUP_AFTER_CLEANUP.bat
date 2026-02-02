@echo off
cls
echo.
echo ========================================
echo  SETUP AFTER CLEANUP
echo ========================================
echo.
echo This will recreate the virtual environment
echo and reinstall all dependencies.
echo.
echo Time required: 2-3 minutes
echo.
pause

REM Create backend virtual environment
echo.
echo [1/2] Creating backend virtual environment...
cd /d "%~dp0backend"
python -m venv .venv
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Install backend dependencies
echo.
echo [2/2] Installing backend dependencies...
.\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\.venv\Scripts\pip.exe install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo Virtual environment created at:
echo   backend\.venv\
echo.
echo All dependencies installed successfully.
echo.
echo You can now run:
echo   RUN_ALL.bat  (to start all components)
echo.
echo Or test backend manually:
echo   cd backend
echo   .\.venv\Scripts\activate
echo   python manage.py check
echo.
pause
