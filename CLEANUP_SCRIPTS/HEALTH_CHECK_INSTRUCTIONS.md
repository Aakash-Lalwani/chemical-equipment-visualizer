# Repository Cleanup - Health Check Scripts
# =========================================
# Run these after cleanup to verify everything still works

---

## 🏥 Post-Cleanup Health Checks

After running cleanup scripts, validate that your project still functions correctly.

---

## 1️⃣ Backend Health Check

Verifies Django backend can run without errors.

### Windows PowerShell:
```powershell
# Navigate to backend directory
cd c:\Users\91985\Desktop\FOSSE_2026\backend

# Recreate virtual environment (if .venv was moved)
Write-Host "🔧 Creating virtual environment..." -ForegroundColor Cyan
python -m venv .venv

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "📦 Installing dependencies (this may take 2-3 minutes)..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# Check for Django issues
Write-Host "🏥 Running Django system check..." -ForegroundColor Cyan
python manage.py check

# Check migrations
Write-Host "🏥 Checking database migrations..." -ForegroundColor Cyan
python manage.py migrate --check

# Try collecting static files (if whitenoise configured)
Write-Host "🏥 Checking static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput --dry-run

# Deactivate
deactivate

Write-Host ""
Write-Host "✅ Backend health check complete!" -ForegroundColor Green
Write-Host ""
```

### Unix/Mac/Linux Bash:
```bash
# Navigate to backend directory
cd ~/path/to/FOSSE_2026/backend

# Recreate virtual environment (if .venv was moved)
echo "🔧 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies (this may take 2-3 minutes)..."
pip install -r requirements.txt --quiet

# Check for Django issues
echo "🏥 Running Django system check..."
python manage.py check

# Check migrations
echo "🏥 Checking database migrations..."
python manage.py migrate --check

# Try collecting static files
echo "🏥 Checking static files..."
python manage.py collectstatic --noinput --dry-run

# Deactivate
deactivate

echo ""
echo "✅ Backend health check complete!"
echo ""
```

**Expected Output:**
```
🔧 Creating virtual environment...
🔧 Activating virtual environment...
📦 Installing dependencies (this may take 2-3 minutes)...
🏥 Running Django system check...
System check identified no issues (0 silenced).

🏥 Checking database migrations...
No migrations to apply.

🏥 Checking static files...
0 static files copied to '/path/to/staticfiles', 120 unmodified.

✅ Backend health check complete!
```

**If You See Errors:**
- `ModuleNotFoundError: No module named 'django'` → Dependencies not installed correctly
  - Solution: `pip install -r requirements.txt` (without --quiet to see progress)
- `ERRORS: settings.DATABASES.default` → Database configuration issue
  - Solution: Check `backend/config/settings.py` database settings
- `CommandError: You must set settings.STATIC_ROOT` → Static files config
  - Solution: Normal if STATIC_ROOT not configured, can ignore

---

## 2️⃣ Frontend Health Check (If Node.js Installed)

Verifies React frontend can build without errors.

### Windows PowerShell:
```powershell
# Navigate to frontend directory
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react

# Check if Node.js is installed
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✅ Node.js found: $(node --version)" -ForegroundColor Green
    
    # Install dependencies (if node_modules was removed)
    if (-not (Test-Path "node_modules")) {
        Write-Host "📦 Installing dependencies (this may take 2-3 minutes)..." -ForegroundColor Cyan
        npm install
    } else {
        Write-Host "✅ node_modules/ exists, skipping install" -ForegroundColor Green
    }
    
    # Try building
    Write-Host "🏥 Building frontend..." -ForegroundColor Cyan
    npm run build
    
    Write-Host ""
    Write-Host "✅ Frontend health check complete!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⏭️  Node.js not installed, skipping frontend check" -ForegroundColor Yellow
    Write-Host "   (This is OK - frontend is optional)" -ForegroundColor Gray
    Write-Host ""
}
```

### Unix/Mac/Linux Bash:
```bash
# Navigate to frontend directory
cd ~/path/to/FOSSE_2026/frontend-react

# Check if Node.js is installed
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
    
    # Install dependencies (if node_modules was removed)
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing dependencies (this may take 2-3 minutes)..."
        npm install
    else
        echo "✅ node_modules/ exists, skipping install"
    fi
    
    # Try building
    echo "🏥 Building frontend..."
    npm run build
    
    echo ""
    echo "✅ Frontend health check complete!"
    echo ""
else
    echo "⏭️  Node.js not installed, skipping frontend check"
    echo "   (This is OK - frontend is optional)"
    echo ""
fi
```

**Expected Output:**
```
✅ Node.js found: v18.17.0
✅ node_modules/ exists, skipping install
🏥 Building frontend...
vite v4.4.5 building for production...
✓ 234 modules transformed.
dist/index.html                  0.45 kB
dist/assets/index-abc123.css     4.23 kB
dist/assets/index-def456.js     142.56 kB
✅ Frontend health check complete!
```

**If You See Errors:**
- `command not found: node` → Node.js not installed
  - Solution: This is expected, frontend is optional. Backend can serve static files.
- `npm ERR! Missing script: "build"` → Build script not defined
  - Solution: Check `package.json` has `"scripts": { "build": "vite build" }`
- Build errors about missing modules → Dependencies not installed
  - Solution: `npm install` then retry `npm run build`

---

## 3️⃣ Desktop App Health Check

Verifies PyQt5 desktop application imports work.

### Windows PowerShell:
```powershell
# Navigate to desktop directory
cd c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt

# Test imports (quick check without launching GUI)
Write-Host "🏥 Testing desktop app imports..." -ForegroundColor Cyan
python -c "
import sys
try:
    import PyQt5
    import matplotlib
    import pandas
    print('✅ All desktop app imports successful')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Desktop app health check complete!" -ForegroundColor Green
} else {
    Write-Host "❌ Desktop app has import issues" -ForegroundColor Red
    Write-Host "   Run: pip install -r desktop-pyqt/requirements.txt" -ForegroundColor Yellow
}

Write-Host ""
```

### Unix/Mac/Linux Bash:
```bash
# Navigate to desktop directory
cd ~/path/to/FOSSE_2026/desktop-pyqt

# Test imports (quick check without launching GUI)
echo "🏥 Testing desktop app imports..."
python3 -c "
import sys
try:
    import PyQt5
    import matplotlib
    import pandas
    print('✅ All desktop app imports successful')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Desktop app health check complete!"
else
    echo "❌ Desktop app has import issues"
    echo "   Run: pip install -r desktop-pyqt/requirements.txt"
fi

echo ""
```

**Expected Output:**
```
🏥 Testing desktop app imports...
✅ All desktop app imports successful
✅ Desktop app health check complete!
```

**If You See Errors:**
- `ModuleNotFoundError: No module named 'PyQt5'` → PyQt5 not installed
  - Solution: `pip install -r desktop-pyqt/requirements.txt`
- `ImportError: DLL load failed` (Windows) → Visual C++ runtime missing
  - Solution: Install Visual C++ Redistributable from Microsoft
- `qt.qpa.plugin: Could not find the Qt platform plugin` → Qt plugins issue
  - Solution: Reinstall PyQt5: `pip uninstall PyQt5; pip install PyQt5`

---

## 4️⃣ Quick Launch Test

Tests if applications actually start (not just import).

### Windows PowerShell:
```powershell
Write-Host "🚀 Testing application launches..." -ForegroundColor Cyan
Write-Host ""

# Test backend
Write-Host "1️⃣  Testing Django backend..." -ForegroundColor Cyan
cd c:\Users\91985\Desktop\FOSSE_2026\backend
Start-Process powershell -ArgumentList "-Command `"cd '$PWD'; .\.venv\Scripts\Activate.ps1; python manage.py runserver --noreload`"" -PassThru | Out-Null
Start-Sleep -Seconds 3

# Check if backend is responding
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000" -TimeoutSec 5 -UseBasicParsing
    Write-Host "   ✅ Backend responding on http://127.0.0.1:8000" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Backend not responding (may need manual start)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "2️⃣  Testing Desktop app..." -ForegroundColor Cyan
Write-Host "   (Will open in new window - close it manually)" -ForegroundColor Gray
cd c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt
Start-Process python -ArgumentList "main.py" -PassThru | Out-Null
Start-Sleep -Seconds 2
Write-Host "   ✅ Desktop app launched (check window)" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Launch test complete!" -ForegroundColor Green
Write-Host "   Remember to stop the backend server (Ctrl+C in its window)" -ForegroundColor Yellow
Write-Host ""
```

### Unix/Mac/Linux Bash:
```bash
echo "🚀 Testing application launches..."
echo ""

# Test backend
echo "1️⃣  Testing Django backend..."
cd ~/path/to/FOSSE_2026/backend
source .venv/bin/activate
python manage.py runserver --noreload &
BACKEND_PID=$!
sleep 3

# Check if backend is responding
if curl -s http://127.0.0.1:8000 > /dev/null; then
    echo "   ✅ Backend responding on http://127.0.0.1:8000"
else
    echo "   ⚠️  Backend not responding"
fi

# Stop backend
kill $BACKEND_PID 2>/dev/null

echo ""
echo "2️⃣  Testing Desktop app..."
echo "   (Will open in new window - close it manually)"
cd ~/path/to/FOSSE_2026/desktop-pyqt
python3 main.py &
sleep 2
echo "   ✅ Desktop app launched (check window)"

echo ""
echo "✅ Launch test complete!"
echo ""
```

---

## 5️⃣ File Structure Verification

Confirms all crucial files still exist after cleanup.

### Windows PowerShell:
```powershell
$RepoRoot = "c:\Users\91985\Desktop\FOSSE_2026"
$CrucialFiles = @(
    "README.md",
    "sample_equipment_data.csv",
    "backend\manage.py",
    "backend\requirements.txt",
    "backend\db.sqlite3",
    "backend\config\settings.py",
    "backend\equipment\models.py",
    "frontend-react\package.json",
    "frontend-react\src\App.jsx",
    "desktop-pyqt\main.py",
    "desktop-pyqt\styles.py",
    "desktop-pyqt\requirements.txt"
)

Write-Host "🔍 Verifying crucial files..." -ForegroundColor Cyan
Write-Host ""

$AllPresent = $true
foreach ($File in $CrucialFiles) {
    $FullPath = Join-Path $RepoRoot $File
    if (Test-Path $FullPath) {
        Write-Host "   ✅ $File" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $File (MISSING!)" -ForegroundColor Red
        $AllPresent = $false
    }
}

Write-Host ""
if ($AllPresent) {
    Write-Host "✅ All crucial files verified!" -ForegroundColor Green
} else {
    Write-Host "❌ Some crucial files are missing!" -ForegroundColor Red
    Write-Host "   Restore from backup immediately!" -ForegroundColor Yellow
}
Write-Host ""
```

### Unix/Mac/Linux Bash:
```bash
REPO_ROOT=~/path/to/FOSSE_2026
CRUCIAL_FILES=(
    "README.md"
    "sample_equipment_data.csv"
    "backend/manage.py"
    "backend/requirements.txt"
    "backend/db.sqlite3"
    "backend/config/settings.py"
    "backend/equipment/models.py"
    "frontend-react/package.json"
    "frontend-react/src/App.jsx"
    "desktop-pyqt/main.py"
    "desktop-pyqt/styles.py"
    "desktop-pyqt/requirements.txt"
)

echo "🔍 Verifying crucial files..."
echo ""

ALL_PRESENT=true
for FILE in "${CRUCIAL_FILES[@]}"; do
    FULL_PATH="$REPO_ROOT/$FILE"
    if [ -e "$FULL_PATH" ]; then
        echo "   ✅ $FILE"
    else
        echo "   ❌ $FILE (MISSING!)"
        ALL_PRESENT=false
    fi
done

echo ""
if [ "$ALL_PRESENT" = true ]; then
    echo "✅ All crucial files verified!"
else
    echo "❌ Some crucial files are missing!"
    echo "   Restore from backup immediately!"
fi
echo ""
```

---

## 🎯 All-in-One Health Check Script

Run all checks in sequence.

### Windows PowerShell (`CLEANUP_SCRIPTS/health_check_all.ps1`):
```powershell
# Save this as health_check_all.ps1 in CLEANUP_SCRIPTS folder
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🏥 COMPREHENSIVE HEALTH CHECK" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Run all health checks
. "$PSScriptRoot\health_check_backend.ps1"
. "$PSScriptRoot\health_check_frontend.ps1"
. "$PSScriptRoot\health_check_desktop.ps1"
. "$PSScriptRoot\health_check_files.ps1"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "✅ ALL HEALTH CHECKS COMPLETE" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
```

---

## 🔧 Troubleshooting Common Issues

### Issue: "python: command not found"
**Solution:**
- Windows: Install Python from https://www.python.org/downloads/
- Ensure Python is in PATH: `python --version`
- Use `py` instead of `python` on Windows

### Issue: Virtual environment activation fails
**Solution:**
- Windows: Run PowerShell as Administrator
- Enable script execution: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Alternative: Use `python -m venv .venv` then `.\.venv\Scripts\python.exe` directly

### Issue: Dependencies fail to install
**Solution:**
- Check internet connection
- Update pip: `python -m pip install --upgrade pip`
- Try installing one-by-one: `pip install django djangorestframework pandas`
- Check for conflicting Python versions: `python --version`

### Issue: "Database is locked"
**Solution:**
- Close all Python/Django processes
- Check for zombie processes: Task Manager (Windows) or `ps aux | grep python` (Unix)
- Restart computer if needed
- Last resort: Delete `db.sqlite3-journal` (not `db.sqlite3`!)

### Issue: Desktop app won't start (Qt errors)
**Solution:**
- Reinstall PyQt5: `pip uninstall PyQt5; pip install PyQt5`
- Install Qt dependencies (Unix): `sudo apt-get install python3-pyqt5`
- Try running in terminal to see error messages: `python desktop-pyqt/main.py`

---

## ✅ Success Criteria

Your cleanup was successful if:

- [ ] ✅ Backend Django check passes (no errors)
- [ ] ✅ Backend migrations check passes
- [ ] ✅ Frontend builds without errors (or Node.js not installed = OK)
- [ ] ✅ Desktop app imports work
- [ ] ✅ All crucial files verified present
- [ ] ✅ Can start backend server (http://127.0.0.1:8000 accessible)
- [ ] ✅ Can launch desktop app GUI

If any check fails, restore from backup and investigate.

---

## 🚨 Emergency Restoration

If health checks fail and you need to restore:

### From cleanup_backup/:
```powershell
# Windows - Restore everything
Copy-Item -Path "cleanup_backup\20260127_HHMMSS\*" -Destination "." -Recurse -Force

# Unix/Mac - Restore everything
cp -r cleanup_backup/20260127_HHMMSS/* .
```

### From Git backup:
```bash
git checkout cleanup-backup-20260127-HHMMSS
# Verify files are back
git checkout main
```

### From Zip backup:
```powershell
# Windows
Expand-Archive -Path "repo-backup-20260127-HHMMSS.zip" -DestinationPath "restored_backup"
# Then manually copy files back

# Unix/Mac
unzip repo-backup-20260127-HHMMSS.zip -d restored_backup/
# Then manually copy files back
```

---

**Last Updated:** 2026-01-27  
**For Support:** Refer to CLEANUP_DRY_RUN_REPORT.md for detailed cleanup information
