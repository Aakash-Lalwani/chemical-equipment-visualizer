#!/usr/bin/env python3
"""
Repository Cleanup - MOVE MODE
================================
Moves cleanup targets to a timestamped backup directory.

Safety Features:
- Creates cleanup_backup/YYYYMMDD_HHMMSS/ directory
- Moves (doesn't delete) files
- Logs all operations
- Validates crucial files before proceeding
- Can be easily reversed
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def format_size(bytes_size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def get_dir_size(path):
    """Calculate total size of directory"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                try:
                    total += entry.stat(follow_symlinks=False).st_size
                except (OSError, PermissionError):
                    pass
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except (OSError, PermissionError):
        pass
    return total

def validate_crucial_files(repo_root):
    """Validate that crucial files exist before proceeding"""
    crucial_files = [
        'README.md',
        'sample_equipment_data.csv',
        'backend/manage.py',
        'backend/requirements.txt',
        'backend/db.sqlite3',
        'frontend-react/package.json',
        'frontend-react/src',
        'desktop-pyqt/main.py',
        'desktop-pyqt/styles.py',
    ]
    
    missing = []
    for file_path in crucial_files:
        full_path = repo_root / file_path
        if not full_path.exists():
            missing.append(file_path)
    
    return missing

def main():
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 70)
    print("🧹 REPOSITORY CLEANUP - MOVE MODE")
    print("=" * 70)
    print(f"{Colors.ENDC}")
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    print(f"📁 Repository Root: {Colors.BOLD}{repo_root}{Colors.ENDC}\n")
    
    # Validate crucial files first
    print(f"{Colors.BOLD}🔍 Validating crucial files...{Colors.ENDC}")
    missing_files = validate_crucial_files(repo_root)
    
    if missing_files:
        print(f"\n{Colors.RED}❌ ERROR: Missing crucial files!{Colors.ENDC}")
        print(f"\nThe following required files were not found:")
        for file in missing_files:
            print(f"  • {file}")
        print(f"\n{Colors.YELLOW}⚠️  Cleanup aborted to prevent data loss{Colors.ENDC}")
        return 1
    
    print(f"{Colors.GREEN}✅ All crucial files verified{Colors.ENDC}\n")
    
    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = repo_root / 'cleanup_backup' / timestamp
    log_file = backup_dir / 'moved_files.log'
    
    print(f"{Colors.BOLD}📦 Creating backup directory...{Colors.ENDC}")
    print(f"   {Colors.CYAN}{backup_dir.relative_to(repo_root)}{Colors.ENDC}\n")
    
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to create backup directory: {e}{Colors.ENDC}")
        return 1
    
    # Define cleanup targets
    targets = [
        {
            'path': '.venv',
            'description': 'Root virtual environment'
        },
        {
            'path': 'backend/venv',
            'description': 'Backend duplicate venv'
        },
        {
            'path': 'desktop-pyqt/build',
            'description': 'PyInstaller build cache'
        },
        {
            'path': 'desktop-pyqt/dist',
            'description': 'PyInstaller distribution'
        },
        {
            'path': 'desktop-pyqt/__pycache__',
            'description': 'Desktop app bytecode cache'
        },
        {
            'path': 'EquipmentVisualizer_Distribution',
            'description': 'Old distribution folder'
        },
    ]
    
    # Scan for additional __pycache__ directories
    pycache_dirs = []
    print(f"{Colors.BOLD}🔍 Scanning for __pycache__ directories...{Colors.ENDC}")
    
    for root, dirs, files in os.walk(repo_root):
        rel_root = Path(root).relative_to(repo_root)
        
        # Skip already-listed targets and backup directory
        if any(x in str(rel_root) for x in ['.venv', 'backend/venv', 'backend\\venv', 'cleanup_backup']):
            continue
        
        if '__pycache__' in dirs:
            pycache_path = str(rel_root / '__pycache__')
            pycache_dirs.append({
                'path': pycache_path,
                'description': f'Cache in {rel_root}'
            })
    
    print(f"   Found {len(pycache_dirs)} additional __pycache__ directories\n")
    
    all_targets = targets + pycache_dirs
    
    # Start logging
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"Repository Cleanup Log\n")
        log.write(f"={'=' * 70}\n")
        log.write(f"Timestamp: {datetime.now().isoformat()}\n")
        log.write(f"Repository: {repo_root}\n")
        log.write(f"Backup Directory: {backup_dir}\n")
        log.write(f"{'=' * 70}\n\n")
        
        # Move files
        print(f"{Colors.BOLD}🚀 Starting file operations...{Colors.ENDC}\n")
        
        moved_count = 0
        skipped_count = 0
        total_size = 0
        errors = []
        
        for i, target in enumerate(all_targets, 1):
            source = repo_root / target['path']
            
            if not source.exists():
                skipped_count += 1
                log.write(f"[SKIP] {target['path']} - Does not exist\n")
                continue
            
            # Calculate size before moving
            size = get_dir_size(str(source)) if source.is_dir() else source.stat().st_size
            
            # Determine destination
            dest = backup_dir / target['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Progress indicator
            progress = f"[{i}/{len(all_targets)}]"
            print(f"{Colors.CYAN}{progress}{Colors.ENDC} Moving: {target['path']}")
            print(f"          {Colors.YELLOW}{target['description']}{Colors.ENDC}")
            print(f"          Size: {format_size(size)}")
            
            try:
                # Move the directory/file
                shutil.move(str(source), str(dest))
                
                # Log success
                log.write(f"[OK] {target['path']} -> {dest.relative_to(backup_dir)}\n")
                log.write(f"     Size: {format_size(size)}\n")
                log.write(f"     Time: {datetime.now().isoformat()}\n\n")
                
                moved_count += 1
                total_size += size
                print(f"          {Colors.GREEN}✅ Moved successfully{Colors.ENDC}\n")
                
            except Exception as e:
                error_msg = f"Failed to move {target['path']}: {str(e)}"
                errors.append(error_msg)
                log.write(f"[ERROR] {error_msg}\n\n")
                print(f"          {Colors.RED}❌ Error: {str(e)}{Colors.ENDC}\n")
        
        # Write summary to log
        log.write(f"\n{'=' * 70}\n")
        log.write(f"SUMMARY\n")
        log.write(f"{'=' * 70}\n")
        log.write(f"Items moved: {moved_count}\n")
        log.write(f"Items skipped: {skipped_count}\n")
        log.write(f"Total size freed: {format_size(total_size)}\n")
        log.write(f"Errors: {len(errors)}\n")
        
        if errors:
            log.write(f"\nERROR DETAILS:\n")
            for error in errors:
                log.write(f"  • {error}\n")
    
    # Print final summary
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}📊 CLEANUP COMPLETE{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print()
    print(f"  ✅ Items moved: {Colors.BOLD}{moved_count}{Colors.ENDC}")
    print(f"  ⏭️  Items skipped: {Colors.BOLD}{skipped_count}{Colors.ENDC}")
    print(f"  💾 Space freed: {Colors.BOLD}{Colors.GREEN}{format_size(total_size)}{Colors.ENDC}")
    print(f"  📝 Log file: {Colors.CYAN}{log_file.relative_to(repo_root)}{Colors.ENDC}")
    
    if errors:
        print(f"\n  {Colors.YELLOW}⚠️  {len(errors)} error(s) occurred{Colors.ENDC}")
        print(f"     Check log file for details")
    
    print()
    print(f"{Colors.BOLD}🔄 RESTORATION INSTRUCTIONS{Colors.ENDC}")
    print(f"{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print()
    print(f"  If you need to restore any files:")
    print()
    print(f"  {Colors.YELLOW}# Restore everything:{Colors.ENDC}")
    print(f"  {Colors.CYAN}cp -r cleanup_backup/{timestamp}/* .{Colors.ENDC} (Unix/Mac)")
    print(f"  {Colors.CYAN}xcopy cleanup_backup\\{timestamp}\\* . /E /I /H /Y{Colors.ENDC} (Windows)")
    print()
    print(f"  {Colors.YELLOW}# Restore specific item (e.g., .venv):{Colors.ENDC}")
    print(f"  {Colors.CYAN}cp -r cleanup_backup/{timestamp}/.venv .{Colors.ENDC} (Unix/Mac)")
    print(f"  {Colors.CYAN}xcopy cleanup_backup\\{timestamp}\\.venv . /E /I /H /Y{Colors.ENDC} (Windows)")
    print()
    print(f"  {Colors.GREEN}✨ Cleanup completed successfully!{Colors.ENDC}")
    print()
    
    return 0 if not errors else 2

if __name__ == '__main__':
    try:
        # Safety confirmation
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  WARNING{Colors.ENDC}")
        print(f"{Colors.YELLOW}This will move ~434 MB of files to cleanup_backup/{Colors.ENDC}")
        print(f"{Colors.YELLOW}Make sure you have created git and zip backups first!{Colors.ENDC}\n")
        
        response = input(f"{Colors.BOLD}Type 'YES MOVE' to proceed:{Colors.ENDC} ").strip()
        
        if response != 'YES MOVE':
            print(f"\n{Colors.RED}❌ Cleanup cancelled{Colors.ENDC}")
            print(f"{Colors.YELLOW}You must type exactly 'YES MOVE' to proceed{Colors.ENDC}\n")
            sys.exit(0)
        
        print()  # Blank line before starting
        sys.exit(main())
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.ENDC}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
