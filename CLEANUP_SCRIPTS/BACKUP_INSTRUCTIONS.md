# Repository Cleanup - Backup Instructions
# =========================================

This document provides step-by-step instructions for creating backups before cleanup.

---

## 📋 Backup Checklist

Before running any cleanup scripts, complete ALL three backup methods:

- [ ] **Git Backup Branch** - Creates a commit with current state
- [ ] **Zip Backup** - Creates a compressed archive of repository
- [ ] **Manual Verification** - Confirm backups exist and are accessible

---

## 1️⃣ Git Backup Branch

Creates a timestamped git branch with current repository state.

### Windows PowerShell:
```powershell
# Navigate to repository root
cd c:\Users\91985\Desktop\FOSSE_2026

# Create timestamp
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

# Create backup branch
git checkout -b "cleanup-backup-$timestamp"

# Stage all changes
git add -A

# Commit (may show "nothing to commit" if no changes - that's OK)
git commit -m "Backup before cleanup - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -a

# Switch back to main branch
git checkout main

# Verify backup branch exists
git branch | Select-String "cleanup-backup"
```

### Unix/Mac/Linux Bash:
```bash
# Navigate to repository root
cd ~/path/to/FOSSE_2026

# Create backup branch
timestamp=$(date +%Y%m%d-%H%M%S)
git checkout -b "cleanup-backup-$timestamp"

# Stage all changes
git add -A

# Commit (may show "nothing to commit" if no changes - that's OK)
git commit -m "Backup before cleanup - $(date)" -a || echo "Nothing new to commit"

# Switch back to main branch
git checkout main

# Verify backup branch exists
git branch | grep "cleanup-backup"
```

**Expected Output:**
```
Switched to a new branch 'cleanup-backup-20260127-143052'
[cleanup-backup-20260127-143052 abc1234] Backup before cleanup - 2026-01-27 14:30:52
Switched to branch 'main'
* cleanup-backup-20260127-143052
```

**To Restore from Git Backup Later:**
```bash
git checkout cleanup-backup-20260127-143052
# Inspect files, then:
git checkout main  # Switch back
```

---

## 2️⃣ Zip Backup

Creates a compressed archive of the entire repository.

### Windows PowerShell:
```powershell
# Navigate to repository root
cd c:\Users\91985\Desktop\FOSSE_2026

# Create timestamp
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$zipName = "repo-backup-$timestamp.zip"

# Create zip (excluding large/unnecessary files)
$excludePaths = @('.git', 'node_modules', '.venv', 'venv', 'cleanup_backup')
$files = Get-ChildItem -Path . -Recurse -Force | 
         Where-Object { 
             $exclude = $false
             foreach ($ex in $excludePaths) {
                 if ($_.FullName -like "*\$ex\*" -or $_.FullName -like "*\$ex") {
                     $exclude = $true
                     break
                 }
             }
             -not $exclude
         }

# Compress (may take 1-2 minutes)
Write-Host "Creating backup zip... This may take a minute..."
Compress-Archive -Path $files.FullName -DestinationPath $zipName -Force

# Verify zip was created
if (Test-Path $zipName) {
    $size = (Get-Item $zipName).Length / 1MB
    Write-Host "✅ Backup created: $zipName ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "❌ Error: Backup zip was not created" -ForegroundColor Red
}
```

### Unix/Mac/Linux Bash:
```bash
# Navigate to repository root
cd ~/path/to/FOSSE_2026

# Create timestamp
timestamp=$(date +%Y%m%d-%H%M%S)
zip_name="repo-backup-$timestamp.zip"

# Create zip (excluding large/unnecessary files)
echo "Creating backup zip... This may take a minute..."
zip -r "$zip_name" . \
    -x "*.git/*" \
    -x "*node_modules/*" \
    -x "*.venv/*" \
    -x "*venv/*" \
    -x "*cleanup_backup/*" \
    -x "*.DS_Store" \
    -x "*__pycache__/*"

# Verify zip was created
if [ -f "$zip_name" ]; then
    size=$(du -h "$zip_name" | cut -f1)
    echo "✅ Backup created: $zip_name ($size)"
else
    echo "❌ Error: Backup zip was not created"
fi
```

**Expected Output:**
```
Creating backup zip... This may take a minute...
  adding: README.md (deflated 65%)
  adding: backend/ (stored 0%)
  adding: backend/manage.py (deflated 58%)
  ...
  [many more files]
  ...
✅ Backup created: repo-backup-20260127-143235.zip (45.32 MB)
```

**Backup zip location:** `c:\Users\91985\Desktop\FOSSE_2026\repo-backup-TIMESTAMP.zip`

**To Restore from Zip Backup Later:**

Windows:
```powershell
Expand-Archive -Path "repo-backup-20260127-143235.zip" -DestinationPath "restored_backup" -Force
```

Unix/Mac:
```bash
unzip repo-backup-20260127-143235.zip -d restored_backup/
```

---

## 3️⃣ Manual Verification

After creating backups, verify they exist:

### Windows PowerShell:
```powershell
# Check git branches
Write-Host "=== Git Backup Branches ===" -ForegroundColor Cyan
git branch | Select-String "cleanup-backup"

# Check zip backups
Write-Host ""
Write-Host "=== Zip Backups ===" -ForegroundColor Cyan
Get-ChildItem -Path . -Filter "repo-backup-*.zip" | Format-Table Name, @{Label="Size (MB)";Expression={[math]::Round($_.Length/1MB, 2)}}
```

### Unix/Mac Bash:
```bash
# Check git branches
echo "=== Git Backup Branches ==="
git branch | grep "cleanup-backup"

# Check zip backups
echo ""
echo "=== Zip Backups ==="
ls -lh repo-backup-*.zip
```

**Expected Output:**
```
=== Git Backup Branches ===
  cleanup-backup-20260127-143052

=== Zip Backups ===
Name                                Size (MB)
----                                ---------
repo-backup-20260127-143235.zip     45.32
```

---

## 🛡️ Backup Safety Tips

1. **Multiple Copies**: Create both git and zip backups (redundancy is good!)
2. **External Storage**: Consider copying the zip backup to:
   - External hard drive
   - Cloud storage (Google Drive, OneDrive, Dropbox)
   - Different computer
3. **Verify Size**: Backup zip should be 40-50 MB (excludes .venv but includes source code)
4. **Test Restore**: Before cleanup, try extracting the zip to verify it works
5. **Keep Backups**: Don't delete backups for at least 1 week after cleanup

---

## ⚠️ What's NOT Backed Up

The following are intentionally excluded from zip backups (safe to exclude):

- `.venv/` - Virtual environment (390+ MB, can be recreated)
- `backend/venv/` - Duplicate venv (20+ MB, can be recreated)
- `.git/` - Git repository (already backed up via git branch)
- `node_modules/` - Node packages (not installed yet)
- `cleanup_backup/` - Previous cleanup backups (recursive backup prevention)

These CAN be recreated from source files:
- Virtual environments: `python -m venv .venv; pip install -r backend/requirements.txt`
- Node modules: `cd frontend-react; npm install`
- Git history: Already in `.git/` folder (separate git backup captures this)

---

## ✅ After Creating Backups

Once you've completed ALL backup steps above:

1. Verify both backups exist (git branch + zip file)
2. Note down the backup branch name: `cleanup-backup-YYYYMMDD-HHMMSS`
3. Note down the zip file name: `repo-backup-YYYYMMDD-HHMMSS.zip`
4. Proceed to cleanup scripts:
   ```powershell
   # Dry run first (preview only)
   python CLEANUP_SCRIPTS/cleanup_dryrun.py
   
   # Or Windows PowerShell version
   .\CLEANUP_SCRIPTS\cleanup_ps.ps1 -DryRun
   ```

5. After reviewing dry run, proceed with actual cleanup (requires "YES MOVE" confirmation):
   ```powershell
   python CLEANUP_SCRIPTS/cleanup_move.py
   
   # Or Windows PowerShell version
   .\CLEANUP_SCRIPTS\cleanup_ps.ps1 -Move
   ```

---

## 🔧 Troubleshooting

### "git: command not found"
- **Solution**: Install Git from https://git-scm.com/downloads
- **Alternative**: Skip git backup, rely on zip backup only

### "zip: command not found" (Unix)
- **Solution**: Install zip: `sudo apt install zip` (Ubuntu) or `brew install zip` (Mac)
- **Alternative**: Use PowerShell on Windows, or tar instead: `tar -czf backup.tar.gz .`

### "Compress-Archive: file too large"
- **Solution**: Exclude more directories:
  ```powershell
  # Add to $excludePaths array
  $excludePaths += @('desktop-pyqt\build', 'desktop-pyqt\dist')
  ```

### Zip backup is 0 bytes or very small
- **Cause**: All files were excluded
- **Solution**: Review exclude patterns, ensure source files are included

---

## 📝 Backup Log Template

Copy this to a text file to track your backups:

```
Repository Backup Log
=====================
Date: 2026-01-27
Repository: c:\Users\91985\Desktop\FOSSE_2026

Git Backup:
- Branch name: cleanup-backup-20260127-143052
- Commit hash: abc123def456
- Created: 2026-01-27 14:30:52

Zip Backup:
- File name: repo-backup-20260127-143235.zip
- File size: 45.32 MB
- Location: c:\Users\91985\Desktop\FOSSE_2026\
- Created: 2026-01-27 14:32:35

External Copies:
- [ ] USB drive (E:\backups\)
- [ ] Google Drive
- [ ] OneDrive

Verification:
- [x] Git branch exists
- [x] Zip file exists and readable
- [x] Zip file size reasonable (40-50 MB)
- [ ] Test extraction successful

Ready for cleanup: YES / NO
```

---

**Next Step:** After creating backups, run `cleanup_dryrun.py` to preview what will be cleaned.
