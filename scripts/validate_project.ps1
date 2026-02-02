# Project Validation Script for Chemical Equipment Visualizer
# Runs comprehensive checks to ensure project is ready for submission
# Usage: .\scripts\validate_project.ps1

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " CHEMICAL EQUIPMENT VISUALIZER" -ForegroundColor Cyan
Write-Host " Project Validation Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0
$WarningCount = 0
$projectRoot = "c:\Users\91985\Desktop\FOSSE_2026"

# Change to project root
Set-Location $projectRoot

# ===========================================
# CHECK 1: Required Files Exist
# ===========================================
Write-Host "[1/8] Checking Required Files..." -ForegroundColor Yellow

$requiredFiles = @(
    "README.md",
    "sample_equipment_data.csv",
    "backend\.env.example",
    "frontend-react\.env.example",
    "desktop-pyqt\config.example.py",
    "backend\requirements.txt",
    "frontend-react\package.json",
    ".gitignore"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Missing: $file" -ForegroundColor Red
        $ErrorCount++
    }
}

# ===========================================
# CHECK 2: Sample CSV Validation
# ===========================================
Write-Host ""
Write-Host "[2/8] Validating Sample CSV..." -ForegroundColor Yellow

if (Test-Path "sample_equipment_data.csv") {
    $csvContent = Get-Content "sample_equipment_data.csv" -Head 1
    if ($csvContent -match "Equipment Name.*Type.*Flowrate.*Pressure.*Temperature") {
        Write-Host "  ✅ CSV headers are correct" -ForegroundColor Green
        
        $lineCount = (Get-Content "sample_equipment_data.csv" | Measure-Object -Line).Lines
        if ($lineCount -gt 1) {
            Write-Host "  ✅ CSV contains $lineCount lines (including header)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ CSV appears to be empty (no data rows)" -ForegroundColor Red
            $ErrorCount++
        }
    } else {
        Write-Host "  ❌ CSV headers are incorrect" -ForegroundColor Red
        Write-Host "     Expected: Equipment Name,Type,Flowrate,Pressure,Temperature" -ForegroundColor Gray
        Write-Host "     Found: $csvContent" -ForegroundColor Gray
        $ErrorCount++
    }
} else {
    Write-Host "  ❌ sample_equipment_data.csv not found" -ForegroundColor Red
    $ErrorCount++
}

# ===========================================
# CHECK 3: Backend Virtual Environment
# ===========================================
Write-Host ""
Write-Host "[3/8] Checking Backend Environment..." -ForegroundColor Yellow

Set-Location "$projectRoot\backend"

if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "  ✅ Virtual environment exists" -ForegroundColor Green
    
    # Check Python version
    $pythonVersion = & .venv\Scripts\python.exe --version 2>&1
    Write-Host "  ℹ️  Python version: $pythonVersion" -ForegroundColor Cyan
    
} else {
    Write-Host "  ❌ Virtual environment not found at backend\.venv" -ForegroundColor Red
    Write-Host "     Run: python -m venv .venv" -ForegroundColor Gray
    $ErrorCount++
}

# ===========================================
# CHECK 4: Backend Dependencies
# ===========================================
Write-Host ""
Write-Host "[4/8] Checking Backend Dependencies..." -ForegroundColor Yellow

if (Test-Path ".venv\Scripts\activate.ps1") {
    & .venv\Scripts\activate.ps1
    
    $requiredPackages = @("django", "djangorestframework", "pandas", "reportlab", "matplotlib")
    
    foreach ($pkg in $requiredPackages) {
        $installed = & .venv\Scripts\pip.exe show $pkg 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ $pkg installed" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $pkg not installed" -ForegroundColor Red
            $ErrorCount++
        }
    }
} else {
    Write-Host "  ⚠️  Cannot check dependencies - venv not activated" -ForegroundColor Yellow
    $WarningCount++
}

# ===========================================
# CHECK 5: Django Configuration
# ===========================================
Write-Host ""
Write-Host "[5/8] Running Django System Checks..." -ForegroundColor Yellow

if (Test-Path ".venv\Scripts\python.exe") {
    $checkOutput = & .venv\Scripts\python.exe manage.py check 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Django system checks passed" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Django system checks failed" -ForegroundColor Red
        Write-Host $checkOutput -ForegroundColor Gray
        $ErrorCount++
    }
} else {
    Write-Host "  ⚠️  Skipping - Python not found" -ForegroundColor Yellow
    $WarningCount++
}

# ===========================================
# CHECK 6: Django Tests
# ===========================================
Write-Host ""
Write-Host "[6/8] Running Django Tests..." -ForegroundColor Yellow

if (Test-Path ".venv\Scripts\python.exe") {
    $testOutput = & .venv\Scripts\python.exe manage.py test 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ All Django tests passed" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Django tests failed" -ForegroundColor Red
        Write-Host $testOutput -ForegroundColor Gray
        $ErrorCount++
    }
} else {
    Write-Host "  ⚠️  Skipping - Python not found" -ForegroundColor Yellow
    $WarningCount++
}

Set-Location $projectRoot

# ===========================================
# CHECK 7: Frontend Dependencies
# ===========================================
Write-Host ""
Write-Host "[7/8] Checking Frontend Dependencies..." -ForegroundColor Yellow

Set-Location "$projectRoot\frontend-react"

if (Test-Path "package.json") {
    Write-Host "  ✅ package.json found" -ForegroundColor Green
    
    if (Test-Path "node_modules") {
        Write-Host "  ✅ node_modules exists" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  node_modules not found - run 'npm install'" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host "  ❌ package.json not found" -ForegroundColor Red
    $ErrorCount++
}

Set-Location $projectRoot

# ===========================================
# CHECK 8: Git Repository Status
# ===========================================
Write-Host ""
Write-Host "[8/8] Checking Git Repository..." -ForegroundColor Yellow

$gitStatus = git status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Git repository initialized" -ForegroundColor Green
    
    # Check if there are uncommitted changes
    $uncommittedFiles = git status --porcelain 2>&1
    if ($uncommittedFiles) {
        $fileCount = ($uncommittedFiles | Measure-Object -Line).Lines
        Write-Host "  ℹ️  $fileCount uncommitted file(s)" -ForegroundColor Cyan
    } else {
        Write-Host "  ✅ No uncommitted changes" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ Not a git repository" -ForegroundColor Red
    $ErrorCount++
}

# ===========================================
# FINAL REPORT
# ===========================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

if ($ErrorCount -eq 0 -and $WarningCount -eq 0) {
    Write-Host "🎉 ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host "   Project is ready for submission" -ForegroundColor Green
} elseif ($ErrorCount -eq 0) {
    Write-Host "✅ CHECKS PASSED (with $WarningCount warning(s))" -ForegroundColor Yellow
    Write-Host "   Project is functional but has minor issues" -ForegroundColor Yellow
} else {
    Write-Host "❌ VALIDATION FAILED" -ForegroundColor Red
    Write-Host "   Found $ErrorCount error(s) and $WarningCount warning(s)" -ForegroundColor Red
    Write-Host "   Fix issues above before submission" -ForegroundColor Red
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Exit with error code if there are errors
if ($ErrorCount -gt 0) {
    exit 1
} else {
    exit 0
}
