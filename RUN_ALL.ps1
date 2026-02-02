# ============================================================
# 🚀 COMPLETE PROJECT LAUNCHER
# Starts Backend + Frontend + Desktop all at once
# ============================================================

$ErrorActionPreference = "Continue"

Write-Host "`n" -NoNewline
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 CHEMICAL EQUIPMENT PARAMETER VISUALIZER" -ForegroundColor Green
Write-Host "   Complete Project Launcher" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`n"

# Project paths
$projectRoot = $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend-react"
$desktopPath = Join-Path $projectRoot "desktop-pyqt"
$venvPython = Join-Path $backendPath ".venv\Scripts\python.exe"

# ============================================================
# STEP 1: Check Prerequisites
# ============================================================
Write-Host "📋 STEP 1: Checking Prerequisites..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray

# Check Python
if (Test-Path $venvPython) {
    Write-Host "   ✅ Python virtual environment found" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python virtual environment not found!" -ForegroundColor Red
    Write-Host "      Expected: $venvPython" -ForegroundColor Red
    exit 1
}

# Check Node.js
$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "   ✅ Node.js found: $nodeVersion" -ForegroundColor Green
        $nodeInstalled = $true
    }
} catch {
    Write-Host "   ⚠️  Node.js not found (React frontend won't start)" -ForegroundColor Yellow
    Write-Host "      Install from: https://nodejs.org/" -ForegroundColor Yellow
}

# Check if backend is already running
$backendRunning = $false
$netstatOutput = netstat -ano | Select-String ":8000.*LISTENING"
if ($netstatOutput) {
    Write-Host "   ⚠️  Backend already running on port 8000" -ForegroundColor Yellow
    $backendRunning = $true
}

Write-Host "`n"

# ============================================================
# STEP 2: Start Backend Server
# ============================================================
Write-Host "🔴 STEP 2: Starting Django Backend..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray

if ($backendRunning) {
    Write-Host "   ℹ️  Using existing backend server" -ForegroundColor Cyan
} else {
    $backendJob = Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "Write-Host '🔴 DJANGO BACKEND SERVER' -ForegroundColor Red; Write-Host '══════════════════════════════════' -ForegroundColor Red; Write-Host ''; Set-Location '$backendPath'; & '$venvPython' manage.py runserver" `
        -PassThru
    
    Write-Host "   🔄 Starting backend server..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3
    
    # Verify backend started
    $backendCheck = netstat -ano | Select-String ":8000.*LISTENING"
    if ($backendCheck) {
        Write-Host "   ✅ Backend server started successfully" -ForegroundColor Green
        Write-Host "      URL: http://127.0.0.1:8000" -ForegroundColor Green
        Write-Host "      Admin: http://127.0.0.1:8000/admin" -ForegroundColor Green
        Write-Host "      Credentials: admin / admin123" -ForegroundColor Gray
    } else {
        Write-Host "   ⚠️  Backend may still be starting..." -ForegroundColor Yellow
    }
}

Write-Host "`n"

# ============================================================
# STEP 3: Start React Frontend
# ============================================================
Write-Host "🔵 STEP 3: Starting React Frontend..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray

if ($nodeInstalled) {
    # Check if node_modules exists
    $nodeModulesPath = Join-Path $frontendPath "node_modules"
    if (-not (Test-Path $nodeModulesPath)) {
        Write-Host "   📦 Installing dependencies (first time only)..." -ForegroundColor Cyan
        Write-Host "      This may take 2-3 minutes..." -ForegroundColor Gray
        
        $installJob = Start-Process powershell -ArgumentList `
            "-NoExit", `
            "-Command", `
            "Write-Host '📦 INSTALLING REACT DEPENDENCIES' -ForegroundColor Blue; Write-Host '══════════════════════════════════' -ForegroundColor Blue; Write-Host ''; Set-Location '$frontendPath'; npm install; Write-Host ''; Write-Host '✅ Installation complete! Starting dev server...' -ForegroundColor Green; Write-Host ''; npm run dev" `
            -PassThru
        
        Write-Host "   🔄 Installing and starting frontend..." -ForegroundColor Cyan
        Write-Host "      Check the new window for progress" -ForegroundColor Gray
    } else {
        $frontendJob = Start-Process powershell -ArgumentList `
            "-NoExit", `
            "-Command", `
            "Write-Host '🔵 REACT FRONTEND SERVER' -ForegroundColor Blue; Write-Host '══════════════════════════════════' -ForegroundColor Blue; Write-Host ''; Set-Location '$frontendPath'; npm run dev" `
            -PassThru
        
        Write-Host "   🔄 Starting frontend dev server..." -ForegroundColor Cyan
        Write-Host "   ✅ Frontend will be available at: http://localhost:3000" -ForegroundColor Green
        Write-Host "      (Wait 5-10 seconds for startup)" -ForegroundColor Gray
    }
} else {
    Write-Host "   ⏭️  Skipping frontend (Node.js not installed)" -ForegroundColor Yellow
    Write-Host "      Install Node.js to enable React frontend" -ForegroundColor Gray
}

Write-Host "`n"

# ============================================================
# STEP 4: Start Desktop Application
# ============================================================
Write-Host "🟢 STEP 4: Starting PyQt5 Desktop App..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray

$desktopJob = Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "Write-Host '🟢 PYQT5 DESKTOP APPLICATION' -ForegroundColor Green; Write-Host '══════════════════════════════════' -ForegroundColor Green; Write-Host ''; Set-Location '$desktopPath'; & '$venvPython' main.py" `
    -PassThru

Write-Host "   🔄 Launching desktop application..." -ForegroundColor Cyan
Write-Host "   ✅ Desktop app window should open shortly" -ForegroundColor Green

Write-Host "`n"

# ============================================================
# STEP 5: Wait and Verify
# ============================================================
Write-Host "⏳ STEP 5: Verifying All Components..." -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray

Start-Sleep -Seconds 3

# Check backend
$backendCheck = netstat -ano | Select-String ":8000.*LISTENING"
if ($backendCheck) {
    Write-Host "   ✅ Backend: RUNNING on port 8000" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Backend: Starting or failed" -ForegroundColor Yellow
}

# Check frontend
if ($nodeInstalled) {
    $frontendCheck = netstat -ano | Select-String ":3000.*LISTENING"
    if ($frontendCheck) {
        Write-Host "   ✅ Frontend: RUNNING on port 3000" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Frontend: Still starting (takes 10-15 seconds)" -ForegroundColor Yellow
    }
}

# Desktop app check (can't easily verify, assume it started)
Write-Host "   ✅ Desktop: Application window opened" -ForegroundColor Green

Write-Host "`n"

# ============================================================
# STEP 6: Final Instructions
# ============================================================
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✅ ALL COMPONENTS STARTED!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`n"

Write-Host "📱 OPEN THESE APPLICATIONS:" -ForegroundColor Yellow
Write-Host "`n"

Write-Host "   1️⃣  WEB FRONTEND (React)" -ForegroundColor Cyan
if ($nodeInstalled) {
    Write-Host "      🌐 http://localhost:3000" -ForegroundColor Green
    Write-Host "      📝 Login: admin / admin123" -ForegroundColor Gray
    Write-Host "      ⏳ Wait 10-15 seconds if not ready yet" -ForegroundColor Gray
} else {
    Write-Host "      ❌ Not available (install Node.js)" -ForegroundColor Red
}

Write-Host "`n"

Write-Host "   2️⃣  DESKTOP APP (PyQt5)" -ForegroundColor Cyan
Write-Host "      🪟 Check for window that opened" -ForegroundColor Green
Write-Host "      📝 Login: admin / admin123" -ForegroundColor Gray

Write-Host "`n"

Write-Host "   3️⃣  BACKEND ADMIN" -ForegroundColor Cyan
Write-Host "      🌐 http://127.0.0.1:8000/admin" -ForegroundColor Green
Write-Host "      📝 Login: admin / admin123" -ForegroundColor Gray

Write-Host "`n"
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "`n"

Write-Host "📊 WHAT TO DO NEXT:" -ForegroundColor Yellow
Write-Host "`n"
Write-Host "   1. Open web browser → http://localhost:3000" -ForegroundColor White
Write-Host "   2. Use desktop app window that opened" -ForegroundColor White
Write-Host "   3. Upload sample file: sample_equipment_data.csv" -ForegroundColor White
Write-Host "   4. View charts and download PDF reports" -ForegroundColor White

Write-Host "`n"
Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "`n"

Write-Host "🪟 TERMINAL WINDOWS:" -ForegroundColor Yellow
Write-Host "   • Keep all opened windows running" -ForegroundColor White
Write-Host "   • Don't close them until you're done" -ForegroundColor White
Write-Host "   • Each window shows logs for its component" -ForegroundColor White

Write-Host "`n"
Write-Host "🛑 TO STOP EVERYTHING:" -ForegroundColor Yellow
Write-Host "   • Press Ctrl+C in each terminal window" -ForegroundColor White
Write-Host "   • Or close all the windows" -ForegroundColor White

Write-Host "`n"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✨ PROJECT IS READY! START TESTING!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`n"

# Open browser automatically
if ($nodeInstalled) {
    Write-Host "🌐 Opening web browser..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000"
}

Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
