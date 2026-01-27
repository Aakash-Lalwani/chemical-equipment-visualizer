#!/bin/bash
#
# Repository Cleanup Script (Unix/Linux/Mac)
# ==========================================
# Supports both --dry-run and --move modes
# 
# Usage:
#   ./cleanup_unix.sh --dry-run    # Shows what would be moved
#   ./cleanup_unix.sh --move       # Actually moves files to backup
#

set -euo pipefail  # Exit on error, undefined var, or pipe failure

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Mode
MODE="${1:---dry-run}"

# Cleanup targets
declare -a TARGETS=(
    ".venv:Root virtual environment"
    "backend/venv:Backend duplicate venv"
    "desktop-pyqt/build:PyInstaller build cache"
    "desktop-pyqt/dist:PyInstaller distribution"
    "desktop-pyqt/__pycache__:Desktop bytecode cache"
    "EquipmentVisualizer_Distribution:Old distribution folder"
)

# Crucial files to validate
declare -a CRUCIAL_FILES=(
    "README.md"
    "sample_equipment_data.csv"
    "backend/manage.py"
    "backend/requirements.txt"
    "backend/db.sqlite3"
    "frontend-react/package.json"
    "desktop-pyqt/main.py"
    "desktop-pyqt/styles.py"
)

# Function: Format bytes to human-readable
format_size() {
    local bytes=$1
    if [ "$bytes" -lt 1024 ]; then
        echo "${bytes} B"
    elif [ "$bytes" -lt 1048576 ]; then
        echo "$((bytes / 1024)) KB"
    elif [ "$bytes" -lt 1073741824 ]; then
        echo "$((bytes / 1048576)) MB"
    else
        echo "$((bytes / 1073741824)) GB"
    fi
}

# Function: Get directory size
get_dir_size() {
    local dir="$1"
    if [ -d "$dir" ]; then
        du -sb "$dir" 2>/dev/null | cut -f1 || echo "0"
    else
        echo "0"
    fi
}

# Function: Validate crucial files
validate_crucial_files() {
    echo -e "${BOLD}🔍 Validating crucial files...${NC}"
    local missing=()
    
    for file in "${CRUCIAL_FILES[@]}"; do
        if [ ! -e "$REPO_ROOT/$file" ]; then
            missing+=("$file")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}❌ ERROR: Missing crucial files!${NC}"
        echo -e "\nThe following required files were not found:"
        for file in "${missing[@]}"; do
            echo -e "  • $file"
        done
        echo -e "\n${YELLOW}⚠️  Cleanup aborted to prevent data loss${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All crucial files verified${NC}\n"
}

# Function: Dry run mode
dry_run() {
    echo -e "${BOLD}${CYAN}"
    echo "======================================================================"
    echo "🔍 REPOSITORY CLEANUP - DRY RUN MODE"
    echo "======================================================================"
    echo -e "${NC}"
    echo -e "📁 Repository Root: ${BOLD}$REPO_ROOT${NC}\n"
    
    local total_size=0
    local found_count=0
    
    echo -e "${BOLD}🔍 Scanning targets...${NC}\n"
    
    for target in "${TARGETS[@]}"; do
        IFS=':' read -r path description <<< "$target"
        local full_path="$REPO_ROOT/$path"
        
        if [ -e "$full_path" ]; then
            local size=$(get_dir_size "$full_path")
            total_size=$((total_size + size))
            found_count=$((found_count + 1))
            
            echo -e "  ${GREEN}✓${NC} ${BOLD}$path${NC}"
            echo -e "    $description"
            echo -e "    Size: $(format_size $size)"
            echo
        else
            echo -e "  ${YELLOW}⊘${NC} $path (not found)"
            echo
        fi
    done
    
    # Scan for __pycache__ directories
    echo -e "${BOLD}🔍 Scanning for __pycache__ directories...${NC}"
    local pycache_count=0
    local pycache_size=0
    
    while IFS= read -r -d '' pycache_dir; do
        # Skip .venv and backend/venv
        if [[ "$pycache_dir" == *".venv"* ]] || [[ "$pycache_dir" == *"backend/venv"* ]]; then
            continue
        fi
        
        local size=$(get_dir_size "$pycache_dir")
        pycache_size=$((pycache_size + size))
        pycache_count=$((pycache_count + 1))
    done < <(find "$REPO_ROOT" -type d -name "__pycache__" -print0 2>/dev/null)
    
    echo -e "   Found $pycache_count additional __pycache__ directories ($(format_size $pycache_size))\n"
    
    total_size=$((total_size + pycache_size))
    found_count=$((found_count + pycache_count))
    
    # Summary
    echo -e "${BOLD}${CYAN}======================================================================${NC}"
    echo -e "${BOLD}📊 SUMMARY${NC}"
    echo -e "${BOLD}${CYAN}======================================================================${NC}"
    echo
    echo -e "  🗂️  Directories to move: ${BOLD}$found_count${NC}"
    echo -e "  💾 Total space to free: ${BOLD}${GREEN}$(format_size $total_size)${NC}"
    echo
    echo -e "${GREEN}✅ This was a DRY RUN - No files were moved${NC}"
    echo
    echo -e "To proceed with cleanup:"
    echo -e "  ${CYAN}./cleanup_unix.sh --move${NC}"
    echo
}

# Function: Move mode
move_mode() {
    echo -e "${BOLD}${CYAN}"
    echo "======================================================================"
    echo "🧹 REPOSITORY CLEANUP - MOVE MODE"
    echo "======================================================================"
    echo -e "${NC}"
    echo -e "📁 Repository Root: ${BOLD}$REPO_ROOT${NC}\n"
    
    # Validate crucial files
    validate_crucial_files
    
    # Create backup directory
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="$REPO_ROOT/cleanup_backup/$timestamp"
    local log_file="$backup_dir/moved_files.log"
    
    echo -e "${BOLD}📦 Creating backup directory...${NC}"
    echo -e "   ${CYAN}cleanup_backup/$timestamp${NC}\n"
    
    mkdir -p "$backup_dir"
    
    # Initialize log
    cat > "$log_file" << EOF
Repository Cleanup Log
======================================================================
Timestamp: $(date --iso-8601=seconds 2>/dev/null || date)
Repository: $REPO_ROOT
Backup Directory: $backup_dir
======================================================================

EOF
    
    local moved_count=0
    local skipped_count=0
    local total_size=0
    
    echo -e "${BOLD}🚀 Starting file operations...${NC}\n"
    
    # Move targets
    for target in "${TARGETS[@]}"; do
        IFS=':' read -r path description <<< "$target"
        local source="$REPO_ROOT/$path"
        
        if [ ! -e "$source" ]; then
            skipped_count=$((skipped_count + 1))
            echo "[SKIP] $path - Does not exist" >> "$log_file"
            continue
        fi
        
        local size=$(get_dir_size "$source")
        local dest="$backup_dir/$path"
        
        mkdir -p "$(dirname "$dest")"
        
        echo -e "${CYAN}[$(($moved_count + $skipped_count + 1))/${#TARGETS[@]}]${NC} Moving: $path"
        echo -e "          ${YELLOW}$description${NC}"
        echo -e "          Size: $(format_size $size)"
        
        if mv "$source" "$dest" 2>/dev/null; then
            echo "[OK] $path -> $dest" >> "$log_file"
            echo "     Size: $(format_size $size)" >> "$log_file"
            echo "     Time: $(date --iso-8601=seconds 2>/dev/null || date)" >> "$log_file"
            echo >> "$log_file"
            
            moved_count=$((moved_count + 1))
            total_size=$((total_size + size))
            echo -e "          ${GREEN}✅ Moved successfully${NC}\n"
        else
            echo "[ERROR] Failed to move $path" >> "$log_file"
            echo >> "$log_file"
            echo -e "          ${RED}❌ Error during move${NC}\n"
        fi
    done
    
    # Move __pycache__ directories
    echo -e "${BOLD}🔍 Moving __pycache__ directories...${NC}\n"
    
    while IFS= read -r -d '' pycache_dir; do
        # Skip .venv and backend/venv
        if [[ "$pycache_dir" == *".venv"* ]] || [[ "$pycache_dir" == *"backend/venv"* ]]; then
            continue
        fi
        
        local rel_path="${pycache_dir#$REPO_ROOT/}"
        local size=$(get_dir_size "$pycache_dir")
        local dest="$backup_dir/$rel_path"
        
        mkdir -p "$(dirname "$dest")"
        
        if mv "$pycache_dir" "$dest" 2>/dev/null; then
            echo "[OK] $rel_path -> $dest" >> "$log_file"
            moved_count=$((moved_count + 1))
            total_size=$((total_size + size))
        fi
    done < <(find "$REPO_ROOT" -type d -name "__pycache__" -print0 2>/dev/null)
    
    # Write summary to log
    cat >> "$log_file" << EOF

======================================================================
SUMMARY
======================================================================
Items moved: $moved_count
Items skipped: $skipped_count
Total size freed: $(format_size $total_size)
EOF
    
    # Print summary
    echo -e "${BOLD}${CYAN}======================================================================${NC}"
    echo -e "${BOLD}📊 CLEANUP COMPLETE${NC}"
    echo -e "${BOLD}${CYAN}======================================================================${NC}"
    echo
    echo -e "  ✅ Items moved: ${BOLD}$moved_count${NC}"
    echo -e "  ⏭️  Items skipped: ${BOLD}$skipped_count${NC}"
    echo -e "  💾 Space freed: ${BOLD}${GREEN}$(format_size $total_size)${NC}"
    echo -e "  📝 Log file: ${CYAN}cleanup_backup/$timestamp/moved_files.log${NC}"
    echo
    echo -e "${BOLD}🔄 RESTORATION INSTRUCTIONS${NC}"
    echo -e "${CYAN}======================================================================${NC}"
    echo
    echo -e "  If you need to restore any files:"
    echo
    echo -e "  ${YELLOW}# Restore everything:${NC}"
    echo -e "  ${CYAN}cp -r cleanup_backup/$timestamp/* .${NC}"
    echo
    echo -e "  ${YELLOW}# Restore specific item (e.g., .venv):${NC}"
    echo -e "  ${CYAN}cp -r cleanup_backup/$timestamp/.venv .${NC}"
    echo
    echo -e "  ${GREEN}✨ Cleanup completed successfully!${NC}"
    echo
}

# Main execution
main() {
    cd "$REPO_ROOT"
    
    case "$MODE" in
        --dry-run)
            dry_run
            ;;
        --move)
            echo -e "\n${BOLD}${YELLOW}⚠️  WARNING${NC}"
            echo -e "${YELLOW}This will move ~434 MB of files to cleanup_backup/${NC}"
            echo -e "${YELLOW}Make sure you have created git and zip backups first!${NC}\n"
            
            read -p "$(echo -e ${BOLD})Type 'YES MOVE' to proceed:$(echo -e ${NC}) " response
            
            if [ "$response" != "YES MOVE" ]; then
                echo -e "\n${RED}❌ Cleanup cancelled${NC}"
                echo -e "${YELLOW}You must type exactly 'YES MOVE' to proceed${NC}\n"
                exit 0
            fi
            
            echo
            move_mode
            ;;
        *)
            echo -e "${RED}Invalid mode: $MODE${NC}"
            echo -e "Usage: $0 [--dry-run|--move]"
            exit 1
            ;;
    esac
}

# Run main
main "$@"
