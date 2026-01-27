# Repository Cleanup Script (Windows PowerShell)
# ==============================================
# Supports both -DryRun and -Move modes
# 
# Usage:
#   .\cleanup_ps.ps1 -DryRun    # Shows what would be moved
#   .\cleanup_ps.ps1 -Move      # Actually moves files to backup
#

[CmdletBinding()]
param(
    [Parameter(ParameterSetName='DryRun')]
    [switch]$DryRun,
    
    [Parameter(ParameterSetName='Move')]
    [switch]$Move
)

# Set error action preference
$ErrorActionPreference = 'Stop'

# Get repository root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

# Cleanup targets
$Targets = @(
    @{Path=".venv"; Description="Root virtual environment"}
    @{Path="backend\venv"; Description="Backend duplicate venv"}
    @{Path="desktop-pyqt\build"; Description="PyInstaller build cache"}
    @{Path="desktop-pyqt\dist"; Description="PyInstaller distribution"}
    @{Path="desktop-pyqt\__pycache__"; Description="Desktop bytecode cache"}
    @{Path="EquipmentVisualizer_Distribution"; Description="Old distribution folder"}
)

# Crucial files to validate
$CrucialFiles = @(
    "README.md",
    "sample_equipment_data.csv",
    "backend\manage.py",
    "backend\requirements.txt",
    "backend\db.sqlite3",
    "frontend-react\package.json",
    "desktop-pyqt\main.py",
    "desktop-pyqt\styles.py"
)

# Function: Format bytes to human-readable
function Format-Size {
    param([long]$Bytes)
    
    if ($Bytes -lt 1KB) {
        return "$Bytes B"
    } elseif ($Bytes -lt 1MB) {
        return "{0:N2} KB" -f ($Bytes / 1KB)
    } elseif ($Bytes -lt 1GB) {
        return "{0:N2} MB" -f ($Bytes / 1MB)
    } else {
        return "{0:N2} GB" -f ($Bytes / 1GB)
    }
}

# Function: Get directory size
function Get-DirectorySize {
    param([string]$Path)
    
    if (Test-Path $Path) {
        return (Get-ChildItem -Path $Path -Recurse -Force -ErrorAction SilentlyContinue | 
                Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    }
    return 0
}

# Function: Validate crucial files
function Test-CrucialFiles {
    Write-Host "🔍 Validating crucial files..." -ForegroundColor Cyan -NoNewline
    $Missing = @()
    
    foreach ($File in $CrucialFiles) {
        $FullPath = Join-Path $RepoRoot $File
        if (-not (Test-Path $FullPath)) {
            $Missing += $File
        }
    }
    
    if ($Missing.Count -gt 0) {
        Write-Host ""
        Write-Host "❌ ERROR: Missing crucial files!" -ForegroundColor Red
        Write-Host ""
        Write-Host "The following required files were not found:" -ForegroundColor Yellow
        foreach ($File in $Missing) {
            Write-Host "  • $File" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "⚠️  Cleanup aborted to prevent data loss" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host " ✅" -ForegroundColor Green
    Write-Host ""
}

# Function: Dry run mode
function Invoke-DryRun {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "🔍 REPOSITORY CLEANUP - DRY RUN MODE" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📁 Repository Root: " -NoNewline
    Write-Host $RepoRoot -ForegroundColor White
    Write-Host ""
    
    Write-Host "🔍 Scanning targets..." -ForegroundColor Cyan
    Write-Host ""
    
    $TotalSize = 0
    $FoundCount = 0
    
    foreach ($Target in $Targets) {
        $FullPath = Join-Path $RepoRoot $Target.Path
        
        if (Test-Path $FullPath) {
            $Size = Get-DirectorySize $FullPath
            $TotalSize += $Size
            $FoundCount++
            
            Write-Host "  ✓ " -ForegroundColor Green -NoNewline
            Write-Host $Target.Path -ForegroundColor White
            Write-Host "    $($Target.Description)" -ForegroundColor Gray
            Write-Host "    Size: $(Format-Size $Size)" -ForegroundColor Yellow
            Write-Host ""
        } else {
            Write-Host "  ⊘ $($Target.Path) (not found)" -ForegroundColor Yellow
            Write-Host ""
        }
    }
    
    # Scan for __pycache__ directories
    Write-Host "🔍 Scanning for __pycache__ directories..." -ForegroundColor Cyan
    
    $PyCacheDirs = Get-ChildItem -Path $RepoRoot -Recurse -Force -ErrorAction SilentlyContinue |
                   Where-Object { $_.PSIsContainer -and $_.Name -eq '__pycache__' -and 
                                  $_.FullName -notlike "*\.venv\*" -and 
                                  $_.FullName -notlike "*\backend\venv\*" }
    
    $PyCacheSize = ($PyCacheDirs | ForEach-Object { Get-DirectorySize $_.FullName } | Measure-Object -Sum).Sum
    
    Write-Host "   Found $($PyCacheDirs.Count) additional __pycache__ directories ($(Format-Size $PyCacheSize))" -ForegroundColor Gray
    Write-Host ""
    
    $TotalSize += $PyCacheSize
    $FoundCount += $PyCacheDirs.Count
    
    # Summary
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "📊 SUMMARY" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  🗂️  Directories to move: " -NoNewline
    Write-Host $FoundCount -ForegroundColor White
    Write-Host "  💾 Total space to free: " -NoNewline
    Write-Host (Format-Size $TotalSize) -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ This was a DRY RUN - No files were moved" -ForegroundColor Green
    Write-Host ""
    Write-Host "To proceed with cleanup:"
    Write-Host "  .\cleanup_ps.ps1 -Move" -ForegroundColor Cyan
    Write-Host ""
}

# Function: Move mode
function Invoke-Move {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "🧹 REPOSITORY CLEANUP - MOVE MODE" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📁 Repository Root: " -NoNewline
    Write-Host $RepoRoot -ForegroundColor White
    Write-Host ""
    
    # Validate crucial files
    Test-CrucialFiles
    
    # Create backup directory
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BackupDir = Join-Path $RepoRoot "cleanup_backup\$Timestamp"
    $LogFile = Join-Path $BackupDir "moved_files.log"
    
    Write-Host "📦 Creating backup directory..." -ForegroundColor Cyan
    Write-Host "   cleanup_backup\$Timestamp" -ForegroundColor Gray
    Write-Host ""
    
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    
    # Initialize log
    @"
Repository Cleanup Log
======================================================================
Timestamp: $(Get-Date -Format "o")
Repository: $RepoRoot
Backup Directory: $BackupDir
======================================================================

"@ | Out-File -FilePath $LogFile -Encoding utf8
    
    $MovedCount = 0
    $SkippedCount = 0
    $TotalSize = 0
    
    Write-Host "🚀 Starting file operations..." -ForegroundColor Cyan
    Write-Host ""
    
    # Move targets
    for ($i = 0; $i -lt $Targets.Count; $i++) {
        $Target = $Targets[$i]
        $Source = Join-Path $RepoRoot $Target.Path
        
        if (-not (Test-Path $Source)) {
            $SkippedCount++
            "[SKIP] $($Target.Path) - Does not exist" | Out-File -FilePath $LogFile -Append -Encoding utf8
            continue
        }
        
        $Size = Get-DirectorySize $Source
        $Dest = Join-Path $BackupDir $Target.Path
        $DestParent = Split-Path -Parent $Dest
        
        if (-not (Test-Path $DestParent)) {
            New-Item -ItemType Directory -Path $DestParent -Force | Out-Null
        }
        
        $Progress = "[{0}/{1}]" -f ($i + 1), $Targets.Count
        Write-Host "$Progress Moving: " -ForegroundColor Cyan -NoNewline
        Write-Host $Target.Path -ForegroundColor White
        Write-Host "          $($Target.Description)" -ForegroundColor Yellow
        Write-Host "          Size: $(Format-Size $Size)" -ForegroundColor Gray
        
        try {
            Move-Item -Path $Source -Destination $Dest -Force
            
            @"
[OK] $($Target.Path) -> $Dest
     Size: $(Format-Size $Size)
     Time: $(Get-Date -Format "o")

"@ | Out-File -FilePath $LogFile -Append -Encoding utf8
            
            $MovedCount++
            $TotalSize += $Size
            Write-Host "          ✅ Moved successfully" -ForegroundColor Green
            Write-Host ""
        } catch {
            "[ERROR] Failed to move $($Target.Path): $_`n" | Out-File -FilePath $LogFile -Append -Encoding utf8
            Write-Host "          ❌ Error: $_" -ForegroundColor Red
            Write-Host ""
        }
    }
    
    # Move __pycache__ directories
    Write-Host "🔍 Moving __pycache__ directories..." -ForegroundColor Cyan
    Write-Host ""
    
    $PyCacheDirs = Get-ChildItem -Path $RepoRoot -Recurse -Force -ErrorAction SilentlyContinue |
                   Where-Object { $_.PSIsContainer -and $_.Name -eq '__pycache__' -and 
                                  $_.FullName -notlike "*\.venv\*" -and 
                                  $_.FullName -notlike "*\backend\venv\*" -and
                                  $_.FullName -notlike "*\cleanup_backup\*" }
    
    foreach ($PyCache in $PyCacheDirs) {
        $RelPath = $PyCache.FullName.Replace("$RepoRoot\", "")
        $Size = Get-DirectorySize $PyCache.FullName
        $Dest = Join-Path $BackupDir $RelPath
        $DestParent = Split-Path -Parent $Dest
        
        if (-not (Test-Path $DestParent)) {
            New-Item -ItemType Directory -Path $DestParent -Force | Out-Null
        }
        
        try {
            Move-Item -Path $PyCache.FullName -Destination $Dest -Force
            "[OK] $RelPath -> $Dest`n" | Out-File -FilePath $LogFile -Append -Encoding utf8
            $MovedCount++
            $TotalSize += $Size
        } catch {
            # Silently skip if already moved or inaccessible
        }
    }
    
    # Write summary to log
    @"

======================================================================
SUMMARY
======================================================================
Items moved: $MovedCount
Items skipped: $SkippedCount
Total size freed: $(Format-Size $TotalSize)
"@ | Out-File -FilePath $LogFile -Append -Encoding utf8
    
    # Print summary
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "📊 CLEANUP COMPLETE" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ✅ Items moved: " -NoNewline
    Write-Host $MovedCount -ForegroundColor White
    Write-Host "  ⏭️  Items skipped: " -NoNewline
    Write-Host $SkippedCount -ForegroundColor White
    Write-Host "  💾 Space freed: " -NoNewline
    Write-Host (Format-Size $TotalSize) -ForegroundColor Green
    Write-Host "  📝 Log file: " -NoNewline
    Write-Host "cleanup_backup\$Timestamp\moved_files.log" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔄 RESTORATION INSTRUCTIONS" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  If you need to restore any files:"
    Write-Host ""
    Write-Host "  # Restore everything:" -ForegroundColor Yellow
    Write-Host "  Copy-Item -Path cleanup_backup\$Timestamp\* -Destination . -Recurse -Force" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  # Restore specific item (e.g., .venv):" -ForegroundColor Yellow
    Write-Host "  Copy-Item -Path cleanup_backup\$Timestamp\.venv -Destination . -Recurse -Force" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ✨ Cleanup completed successfully!" -ForegroundColor Green
    Write-Host ""
}

# Main execution
try {
    Set-Location $RepoRoot
    
    if ($DryRun) {
        Invoke-DryRun
    } elseif ($Move) {
        Write-Host ""
        Write-Host "⚠️  WARNING" -ForegroundColor Yellow
        Write-Host "This will move ~434 MB of files to cleanup_backup\" -ForegroundColor Yellow
        Write-Host "Make sure you have created git and zip backups first!" -ForegroundColor Yellow
        Write-Host ""
        
        $Response = Read-Host "Type 'YES MOVE' to proceed"
        
        if ($Response -ne 'YES MOVE') {
            Write-Host ""
            Write-Host "❌ Cleanup cancelled" -ForegroundColor Red
            Write-Host "You must type exactly 'YES MOVE' to proceed" -ForegroundColor Yellow
            Write-Host ""
            exit 0
        }
        
        Invoke-Move
    } else {
        Write-Host "Usage: .\cleanup_ps.ps1 [-DryRun|-Move]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Cyan
        Write-Host "  .\cleanup_ps.ps1 -DryRun    # Preview what will be moved"
        Write-Host "  .\cleanup_ps.ps1 -Move      # Actually move files to backup"
        Write-Host ""
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host $_.ScriptStackTrace -ForegroundColor DarkGray
    exit 1
}
