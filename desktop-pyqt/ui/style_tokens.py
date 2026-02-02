"""
Design Tokens - Color Palette & Spacing

WHAT: Single source of truth for colors and spacing
WHY: Ensures desktop and web look consistent
HOW: Import these tokens instead of hard-coding hex values

Matches frontend-react/src/styles/global.css exactly
"""

# Primary Colors (UPDATED to match web exactly)
PRIMARY = '#2563eb'          # Main brand blue
PRIMARY_DARK = '#1e40af'     # Hover/active state
PRIMARY_LIGHT = '#3b82f6'    # Lighter variant

# Status Colors
SUCCESS = '#10b981'          # Green for success
DANGER = '#ef4444'           # Red for errors
WARNING = '#f59e0b'          # Amber for warnings
INFO = '#3b82f6'             # Blue for info

# Neutral Colors
BG_PRIMARY = '#f9fafb'       # Main background
BG_SECONDARY = '#f3f4f6'     # Secondary background
BG_WHITE = '#ffffff'         # Pure white
BORDER = '#e5e7eb'           # Border color

# Text Colors
TEXT_PRIMARY = '#1f2937'     # Main text (dark gray)
TEXT_SECONDARY = '#6b7280'   # Secondary text (medium gray)
TEXT_LIGHT = '#9ca3af'       # Light text (light gray)

# Chart Colors (for Matplotlib consistency)
CHART_COLORS = [
    '#3b82f6',  # Blue
    '#10b981',  # Green
    '#8b5cf6',  # Purple
    '#f59e0b',  # Orange
    '#ef4444',  # Red
    '#06b6d4',  # Cyan
    '#ec4899',  # Pink
    '#84cc16',  # Lime
]

# Spacing (8px grid system)
SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32
SPACING_2XL = 48

# Border Radius
RADIUS_SM = 4
RADIUS_MD = 8
RADIUS_LG = 12
RADIUS_FULL = 9999

# Typography
FONT_SIZE_XS = 12
FONT_SIZE_SM = 14
FONT_SIZE_BASE = 16
FONT_SIZE_LG = 18
FONT_SIZE_XL = 24
FONT_SIZE_2XL = 32

# Shadows (for QSS - Qt doesn't support box-shadow, use border for subtle effect)
SHADOW_COLOR = 'rgba(0, 0, 0, 0.1)'

# Helper function to get Qt gradient string
def get_gradient(start_color, end_color, direction='diagonal'):
    """
    Generate Qt gradient string
    
    Args:
        start_color: Hex color for start
        end_color: Hex color for end
        direction: 'diagonal', 'vertical', or 'horizontal'
    
    Returns:
        Qt gradient string for QSS
    """
    if direction == 'vertical':
        return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {start_color}, stop:1 {end_color})"
    elif direction == 'horizontal':
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start_color}, stop:1 {end_color})"
    else:  # diagonal
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {start_color}, stop:1 {end_color})"
