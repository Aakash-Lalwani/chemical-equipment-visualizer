# 🧹 Repository Cleanup Scripts

**Purpose:** Safely remove build artifacts, caches, and duplicate virtual environments from your repository.  
**Total Space to Free:** ~434 MB  
**Safety:** 100% - Files are moved to backup, not deleted

---

## 📋 Quick Start Guide

### Step 1: Read the Dry Run Report
```bash
# Already generated for you:
cat CLEANUP_DRY_RUN_REPORT.md
```
This shows exactly what will be moved and why it's safe.

### Step 2: Create Backups (REQUIRED!)
```bash
# Follow detailed instructions in:
cat CLEANUP_SCRIPTS/BACKUP_INSTRUCTIONS.md

# Quick summary:
# 1. Git backup: git checkout -b cleanup-backup-$(date +%Y%m%d-%H%M%S)
# 2. Zip backup: Create compressed archive of repository
```

### Step 3: Run Dry Run (Preview)
```powershell
# Windows PowerShell
.\CLEANUP_SCRIPTS\cleanup_ps.ps1 -DryRun

# Or Python (cross-platform)
python CLEANUP_SCRIPTS/cleanup_dryrun.py
```

### Step 4: Execute Cleanup (Requires "YES MOVE" Confirmation)
```powershell
# Windows PowerShell
.\CLEANUP_SCRIPTS\cleanup_ps.ps1 -Move

# Or Python (cross-platform)
python CLEANUP_SCRIPTS/cleanup_move.py

# Or Unix/Mac
bash CLEANUP_SCRIPTS/cleanup_unix.sh --move
```

### Step 5: Run Health Checks
```bash
# Follow instructions in:
cat CLEANUP_SCRIPTS/HEALTH_CHECK_INSTRUCTIONS.md
```

---

## 📁 Files in This Directory

| File | Description | When to Use |
|------|-------------|-------------|
| **cleanup_dryrun.py** | Python dry run script (preview only) | Run first to see what will be moved |
| **cleanup_move.py** | Python cleanup script (actual move) | After backups, to move files to backup |
| **cleanup_ps.ps1** | PowerShell script (Windows) | Windows alternative to Python scripts |
| **cleanup_unix.sh** | Bash script (Unix/Mac/Linux) | Unix alternative to Python scripts |
| **recommended_gitignore.txt** | Updated .gitignore patterns | Copy to root .gitignore to prevent future clutter |
| **BACKUP_INSTRUCTIONS.md** | Step-by-step backup guide | BEFORE running cleanup |
| **HEALTH_CHECK_INSTRUCTIONS.md** | Post-cleanup verification | AFTER running cleanup |
| **README.md** | This file | Overview and quick reference |

---

## 🎯 What Gets Cleaned Up

### Virtual Environments (416.15 MB)
- `.venv/` - Root virtual environment
- `backend/venv/` - Duplicate backend venv

**Why safe?** Recreate with:
```bash
python -m venv .venv
pip install -r backend/requirements.txt
```

### Build Artifacts (17.81 MB)
- `desktop-pyqt/build/` - PyInstaller build cache
- `desktop-pyqt/dist/` - PyInstaller distribution

**Why safe?** Rebuild with:
```bash
pyinstaller desktop-pyqt/equipment_visualizer.spec
```

### Python Caches (~0.5 MB)
- `__pycache__/` directories (all instances)
- `*.pyc` files (compiled Python bytecode)

**Why safe?** Python auto-regenerates on next run.

### Distribution Artifacts (<1 MB)
- `EquipmentVisualizer_Distribution/` - Old distribution folder

**Why safe?** Contains only README.txt.

---

## 🛡️ What Will NEVER Be Touched

The scripts are designed to protect:

### Essential Files
- ✅ `.git/` - Git repository
- ✅ `README.md`, `LICENSE`
- ✅ `.gitignore` files
- ✅ `sample_equipment_data.csv` (**CRUCIAL demo data**)

### Backend
- ✅ `backend/manage.py`, `backend/requirements.txt`
- ✅ `backend/db.sqlite3` (your database!)
- ✅ `backend/media/` (user uploads!)
- ✅ `backend/equipment/migrations/` (**CRUCIAL database migrations**)
- ✅ All `.py` source files

### Frontend
- ✅ `frontend-react/package.json`, `frontend-react/package-lock.json`
- ✅ `frontend-react/src/`, `frontend-react/public/`
- ✅ All React source code

### Desktop
- ✅ `desktop-pyqt/main.py`, `desktop-pyqt/styles.py`
- ✅ `desktop-pyqt/requirements.txt`, `desktop-pyqt/config.ini`

### Documentation
- ✅ All `*.md` files
- ✅ Test files (`quick_test.py`, etc.)
- ✅ Launch scripts (`RUN_ALL.bat`, etc.)

---

## 🚀 Usage Examples

### Example 1: Windows PowerShell (Recommended for Windows)
```powershell
# 1. Preview what will be cleaned
.\CLEANUP_SCRIPTS\cleanup_ps.ps1 -DryRun

# 2. Create backups (follow BACKUP_INSTRUCTIONS.md)
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
git checkout -b "cleanup-backup-$timestamp"
# ... create zip backup ...

# 3. Run cleanup (requires "YES MOVE" confirmation)
.\CLEANUP_SCRIPTS\cleanup_ps.ps1 -Move

# 4. Verify health (follow HEALTH_CHECK_INSTRUCTIONS.md)
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py check
```

### Example 2: Python (Cross-Platform)
```bash
# 1. Preview
python CLEANUP_SCRIPTS/cleanup_dryrun.py

# 2. Create backups
timestamp=$(date +%Y%m%d-%H%M%S)
git checkout -b "cleanup-backup-$timestamp"
zip -r "repo-backup-$timestamp.zip" . -x "*.git*" -x "*.venv*"

# 3. Run cleanup
python CLEANUP_SCRIPTS/cleanup_move.py
# Type: YES MOVE

# 4. Verify health
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
```

### Example 3: Unix/Mac Bash
```bash
# 1. Make script executable
chmod +x CLEANUP_SCRIPTS/cleanup_unix.sh

# 2. Preview
./CLEANUP_SCRIPTS/cleanup_unix.sh --dry-run

# 3. Create backups
timestamp=$(date +%Y%m%d-%H%M%S)
git checkout -b "cleanup-backup-$timestamp"
zip -r "repo-backup-$timestamp.zip" . -x "*.git*" -x "*.venv*"

# 4. Run cleanup
./CLEANUP_SCRIPTS/cleanup_unix.sh --move
# Type: YES MOVE

# 5. Verify health
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py check
```

---

## 🔄 Restoration Instructions

If something goes wrong, restore from backups:

### Option 1: From cleanup_backup/ (Fastest)
```powershell
# Windows
Copy-Item -Path "cleanup_backup\20260127_143520\*" -Destination "." -Recurse -Force

# Unix/Mac
cp -r cleanup_backup/20260127_143520/* .
```

### Option 2: From Git Backup Branch
```bash
# View backup branches
git branch | grep cleanup-backup

# Switch to backup
git checkout cleanup-backup-20260127-143052

# Verify files, then switch back
git checkout main
```

### Option 3: From Zip Backup
```powershell
# Windows
Expand-Archive -Path "repo-backup-20260127-143520.zip" -DestinationPath "restored"

# Unix/Mac
unzip repo-backup-20260127-143520.zip -d restored/
```

---

## 🔧 Troubleshooting

### "Permission denied" (Windows)
**Solution:**
- Run PowerShell as Administrator
- Close any running applications (backend server, desktop app)
- Check Task Manager for zombie Python processes

### "Cannot remove item: The process cannot access the file"
**Solution:**
- Close VS Code, PyCharm, or other editors
- Stop all running Django/Python processes
- Restart computer if needed

### "python: command not found"
**Solution:**
- Windows: Use `py` instead of `python`
- Install Python: https://www.python.org/downloads/
- Ensure Python in PATH: `python --version`

### Cleanup moves files but health check fails
**Solution:**
- Check `cleanup_backup/TIMESTAMP/moved_files.log` for errors
- Restore specific directories: `cp -r cleanup_backup/.../backend/venv backend/`
- Recreate venv: `python -m venv .venv; pip install -r requirements.txt`

### "ImportError" after cleanup
**Solution:**
- Virtual environment needs recreation: `python -m venv .venv`
- Install dependencies: `pip install -r backend/requirements.txt`
- Verify Python version: `python --version` (should be 3.10+)

---

## 📊 Expected Results

### Before Cleanup
```
Repository Size: ~600 MB
  - .venv/: 394 MB
  - backend/venv/: 22 MB
  - desktop-pyqt/build/: 18 MB
  - Other files: 166 MB
```

### After Cleanup
```
Repository Size: ~166 MB (72% reduction)
  - cleanup_backup/: 434 MB (can be deleted after verification)
  - Source code: 166 MB
Space freed: 434 MB
```

### Cleanup Artifacts
```
cleanup_backup/
└── 20260127_143520/
    ├── .venv/                      (394 MB)
    ├── backend/
    │   └── venv/                   (22 MB)
    ├── desktop-pyqt/
    │   ├── build/                  (18 MB)
    │   ├── dist/                   (0.3 MB)
    │   └── __pycache__/            (0.01 MB)
    ├── EquipmentVisualizer_Distribution/
    └── moved_files.log             (detailed operation log)
```

---

## ⚠️ Safety Guarantees

### What This Cleanup Does:
✅ **Moves** files to `cleanup_backup/TIMESTAMP/`  
✅ Creates detailed log of all operations  
✅ Validates crucial files before proceeding  
✅ Requires explicit "YES MOVE" confirmation  
✅ Provides 3 restoration methods (cleanup_backup, git, zip)

### What This Cleanup Does NOT Do:
❌ Delete files permanently  
❌ Modify source code  
❌ Touch database (`db.sqlite3`)  
❌ Touch user uploads (`media/`)  
❌ Touch migrations  
❌ Touch configuration files  
❌ Touch documentation

---

## 📝 Post-Cleanup Checklist

After running cleanup, verify:

- [ ] Backend starts successfully: `python backend/manage.py runserver`
- [ ] Desktop app launches: `python desktop-pyqt/main.py`
- [ ] Frontend builds (if Node.js installed): `cd frontend-react; npm run build`
- [ ] All tests pass: `python backend/manage.py test`
- [ ] Database intact: `python backend/manage.py migrate --check`
- [ ] Sample data loads: Check `sample_equipment_data.csv`
- [ ] Documentation readable: Check `README.md`

If ANY check fails, restore from backup immediately.

---

## 🎓 ELI5 (Explain Like I'm 5)

**What is cleanup?**  
Your project is like a workshop. Over time, you collect:
- 🧰 Duplicate toolboxes (two venvs = same tools twice)
- 🧱 Half-built Lego sets (build/ folder = messy work in progress)
- 📝 Photocopied instructions (__pycache__ = notes you can rewrite anytime)

We're putting ALL these extras into a labeled box (`cleanup_backup/`) with today's date on it. Your actual work (source code, database, documents) stays exactly where it is.

**Why not delete?**  
Because smart kids don't throw things away—they put them in a box so they can get them back if needed.

**What if I need something back?**  
Three ways:
1. Open the labeled box (`cleanup_backup/`)
2. Look at your photo album (git backup branch)
3. Check your photocopy (zip backup)

**How long does it take?**
- Preview (dry run): 10 seconds
- Creating backups: 2-3 minutes
- Actual cleanup: 30-60 seconds
- Health checks: 3-5 minutes

---

## 📞 Need Help?

1. **Read the dry run report first:** `CLEANUP_DRY_RUN_REPORT.md`
2. **Check backup instructions:** `BACKUP_INSTRUCTIONS.md`
3. **Review health checks:** `HEALTH_CHECK_INSTRUCTIONS.md`
4. **Examine logs:** `cleanup_backup/TIMESTAMP/moved_files.log`
5. **Restore if needed:** Follow restoration instructions above

---

## 🎯 Final Reminders

### BEFORE Running Cleanup:
1. ✅ Read `CLEANUP_DRY_RUN_REPORT.md`
2. ✅ Create git backup branch
3. ✅ Create zip backup
4. ✅ Close all applications
5. ✅ Run dry run to preview

### DURING Cleanup:
1. ✅ Type exactly "YES MOVE" when prompted
2. ✅ Wait for completion (30-60 seconds)
3. ✅ Check for errors in output
4. ✅ Review `moved_files.log`

### AFTER Cleanup:
1. ✅ Run health checks
2. ✅ Test backend: `python manage.py check`
3. ✅ Test desktop app: `python main.py`
4. ✅ Verify crucial files present
5. ✅ Keep backups for 1+ week

---

**Last Updated:** 2026-01-27  
**Version:** 1.0  
**Compatibility:** Windows, Linux, macOS  
**Python Version:** 3.8+

**Ready to proceed?** Reply with "YES MOVE" after creating backups!
