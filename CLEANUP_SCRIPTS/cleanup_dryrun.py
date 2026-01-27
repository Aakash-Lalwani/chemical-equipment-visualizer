#!/usr/bin/env python3
"""
Repository Cleanup - DRY RUN MODE
==================================
Scans the repository and reports what would be moved, without actually moving anything.

Safety: 100% READ-ONLY - No files are modified or moved
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ANSI color codes for terminal output
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

def count_files_recursive(path):
    """Count files in directory recursively"""
    count = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                count += 1
            elif entry.is_dir(follow_symlinks=False):
                count += count_files_recursive(entry.path)
    except (OSError, PermissionError):
        pass
    return count

def main():
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 70)
    print("🔍 REPOSITORY CLEANUP - DRY RUN MODE")
    print("=" * 70)
    print(f"{Colors.ENDC}")
    
    # Get repository root (assumes script is in CLEANUP_SCRIPTS/)
    repo_root = Path(__file__).parent.parent
    print(f"📁 Repository Root: {Colors.BOLD}{repo_root}{Colors.ENDC}\n")
    
    # Define cleanup targets (relative to repo root)
    targets = [
        {
            'path': '.venv',
            'category': 'Virtual Environments',
            'description': 'Root virtual environment'
        },
        {
            'path': 'backend/venv',
            'category': 'Virtual Environments',
            'description': 'Backend duplicate venv'
        },
        {
            'path': 'desktop-pyqt/build',
            'category': 'Build Artifacts',
            'description': 'PyInstaller build cache'
        },
        {
            'path': 'desktop-pyqt/dist',
            'category': 'Build Artifacts',
            'description': 'PyInstaller distribution'
        },
        {
            'path': 'desktop-pyqt/__pycache__',
            'category': 'Python Caches',
            'description': 'Desktop app bytecode cache'
        },
        {
            'path': 'EquipmentVisualizer_Distribution',
            'category': 'Distribution',
            'description': 'Old distribution folder'
        },
    ]
    
    # Scan for additional __pycache__ directories
    pycache_dirs = []
    for root, dirs, files in os.walk(repo_root):
        # Skip .venv and backend/venv (already counted)
        rel_root = Path(root).relative_to(repo_root)
        if '.venv' in str(rel_root) or 'backend\\venv' in str(rel_root) or 'backend/venv' in str(rel_root):
            continue
        
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            pycache_dirs.append({
                'path': str(Path(pycache_path).relative_to(repo_root)),
                'category': 'Python Caches',
                'description': f'Cache in {rel_root}'
            })
    
    # Combine all targets
    all_targets = targets + pycache_dirs
    
    # Categorize and analyze
    categories = {}
    total_size = 0
    total_files = 0
    found_targets = []
    missing_targets = []
    
    print(f"{Colors.BOLD}🔍 Scanning targets...{Colors.ENDC}\n")
    
    for target in all_targets:
        target_path = repo_root / target['path']
        
        if target_path.exists():
            size = get_dir_size(str(target_path))
            files = count_files_recursive(str(target_path))
            
            total_size += size
            total_files += files
            
            if target['category'] not in categories:
                categories[target['category']] = {
                    'size': 0,
                    'files': 0,
                    'items': []
                }
            
            categories[target['category']]['size'] += size
            categories[target['category']]['files'] += files
            categories[target['category']]['items'].append({
                'path': target['path'],
                'description': target['description'],
                'size': size,
                'files': files
            })
            
            found_targets.append(target)
        else:
            missing_targets.append(target)
    
    # Print results by category
    print(f"{Colors.BOLD}{Colors.BLUE}📊 CLEANUP SUMMARY{Colors.ENDC}\n")
    
    for category, data in sorted(categories.items()):
        percentage = (data['size'] / total_size * 100) if total_size > 0 else 0
        print(f"{Colors.BOLD}{Colors.GREEN}▶ {category}{Colors.ENDC}")
        print(f"  Total Size: {Colors.YELLOW}{format_size(data['size'])}{Colors.ENDC} ({percentage:.1f}%)")
        print(f"  Total Files: {Colors.YELLOW}{data['files']:,}{Colors.ENDC}")
        print()
        
        for item in data['items']:
            print(f"    📁 {item['path']}")
            print(f"       {Colors.CYAN}{item['description']}{Colors.ENDC}")
            print(f"       Size: {format_size(item['size'])} | Files: {item['files']:,}")
            print()
    
    # Print overall summary
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}📈 OVERALL TOTALS{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print()
    print(f"  🗂️  Directories to move: {Colors.BOLD}{len(found_targets)}{Colors.ENDC}")
    print(f"  📄 Total files: {Colors.BOLD}{total_files:,}{Colors.ENDC}")
    print(f"  💾 Total space to free: {Colors.BOLD}{Colors.GREEN}{format_size(total_size)}{Colors.ENDC}")
    print()
    
    # Warning about missing targets (expected for first run)
    if missing_targets:
        print(f"{Colors.YELLOW}ℹ️  Note: {len(missing_targets)} targets already cleaned or not present{Colors.ENDC}")
        print()
    
    # Next steps
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}📝 NEXT STEPS{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
    print()
    print(f"  {Colors.GREEN}✅ This was a DRY RUN - No files were moved{Colors.ENDC}")
    print()
    print("  To proceed with cleanup:")
    print()
    print(f"  1. Create backups first:")
    print(f"     {Colors.CYAN}python CLEANUP_SCRIPTS/create_backups.py{Colors.ENDC}")
    print()
    print(f"  2. Run the actual cleanup:")
    print(f"     {Colors.CYAN}python CLEANUP_SCRIPTS/cleanup_move.py{Colors.ENDC}")
    print()
    print(f"  Or use shell scripts:")
    print(f"     {Colors.CYAN}bash CLEANUP_SCRIPTS/cleanup_unix.sh --move{Colors.ENDC} (Unix/Mac)")
    print(f"     {Colors.CYAN}powershell CLEANUP_SCRIPTS/cleanup_ps.ps1 -Move{Colors.ENDC} (Windows)")
    print()
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.ENDC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.ENDC}", file=sys.stderr)
        sys.exit(1)
