"""
Qt Stylesheet - PHASE 3 IMPROVED
Professional styling matching web UI design

WHAT: Modern Qt stylesheet for desktop app
WHY: Match the professional web UI look
HOW: CSS-like styling for Qt widgets
"""

# Color Palette (matching web design - UPDATED to exact web values)
COLORS = {
    'primary': '#2563eb',      # Blue (FIXED: now matches web exactly)
    'primary_dark': '#1e40af',
    'primary_light': '#3b82f6',
    'success': '#10b981',      # Green
    'danger': '#ef4444',       # Red
    'warning': '#f59e0b',      # Amber
    'info': '#3b82f6',         # Blue
    
    'bg': '#f9fafb',           # Light gray background
    'bg_dark': '#f3f4f6',
    'border': '#e5e7eb',       # Border gray
    'text': '#1f2937',         # Dark text
    'text_secondary': '#6b7280', # Gray text
    
    'white': '#ffffff',
    'black': '#000000',
}

# Main Application Stylesheet
MAIN_STYLESHEET = f"""
/* Global Styles */
QWidget {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    color: {COLORS['text']};
}}

/* Main Window */
QMainWindow {{
    background-color: {COLORS['bg']};
}}

/* Push Buttons */
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 14px;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_dark']};
    padding-top: 12px;
    padding-bottom: 8px;
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

QPushButton#successButton {{
    background-color: {COLORS['success']};
}}

QPushButton#successButton:hover {{
    background-color: #059669;
}}

QPushButton#dangerButton {{
    background-color: {COLORS['danger']};
}}

QPushButton#dangerButton:hover {{
    background-color: #dc2626;
}}

QPushButton#secondaryButton {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
}}

QPushButton#secondaryButton:hover {{
    background-color: #e5e7eb;
}}

/* Line Edit (Text Input) */
QLineEdit {{
    background-color: white;
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {COLORS['primary']};
    outline: none;
}}

QLineEdit:disabled {{
    background-color: {COLORS['bg']};
    color: {COLORS['text_secondary']};
}}

/* Labels */
QLabel {{
    color: {COLORS['text']};
}}

QLabel#titleLabel {{
    font-size: 24px;
    font-weight: 700;
    color: {COLORS['text']};
}}

QLabel#subtitleLabel {{
    font-size: 14px;
    color: {COLORS['text_secondary']};
}}

QLabel#headerLabel {{
    font-size: 16px;
    font-weight: 600;
    color: {COLORS['text']};
}}

QLabel#statLabel {{
    font-size: 14px;
    color: {COLORS['text_secondary']};
    font-weight: 500;
}}

QLabel#statValue {{
    font-size: 28px;
    font-weight: 700;
    color: {COLORS['primary']};
}}

QLabel#errorLabel {{
    color: {COLORS['danger']};
    font-size: 13px;
}}

QLabel#successLabel {{
    color: {COLORS['success']};
    font-size: 13px;
}}

QLabel#infoLabel {{
    color: {COLORS['info']};
    font-size: 13px;
}}

/* Group Box */
QGroupBox {{
    background-color: white;
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding: 16px;
    font-weight: 600;
    font-size: 15px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {COLORS['text']};
}}

/* Tab Widget */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: white;
    padding: 16px;
}}

QTabBar::tab {{
    background-color: {COLORS['bg']};
    color: {COLORS['text_secondary']};
    padding: 10px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: white;
    color: {COLORS['primary']};
    font-weight: 600;
    border-bottom: 3px solid {COLORS['primary']};
}}

QTabBar::tab:hover {{
    background-color: {COLORS['bg_dark']};
}}

/* Table Widget */
QTableWidget {{
    background-color: white;
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 8px;
    border: none;
}}

QTableWidget::item:selected {{
    background-color: rgba(59, 130, 246, 0.1);
    color: {COLORS['text']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    padding: 10px;
    border: none;
    border-bottom: 2px solid {COLORS['border']};
    font-weight: 600;
}}

/* List Widget */
QListWidget {{
    background-color: white;
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 4px;
}}

QListWidget::item {{
    padding: 12px;
    border-radius: 4px;
    margin: 2px;
}}

QListWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QListWidget::item:hover {{
    background-color: rgba(59, 130, 246, 0.1);
}}

/* Scroll Bar */
QScrollBar:vertical {{
    border: none;
    background-color: {COLORS['bg']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_secondary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* Message Box */
QMessageBox {{
    background-color: white;
}}

QMessageBox QLabel {{
    color: {COLORS['text']};
    font-size: 14px;
}}
"""

# Login Window Specific Stylesheet
LOGIN_STYLESHEET = f"""
{MAIN_STYLESHEET}

QWidget {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #667eea, stop:1 #764ba2);
}}

QWidget#loginCard {{
    background-color: white;
    border-radius: 12px;
    padding: 40px;
}}

QLabel#appIcon {{
    font-size: 48px;
}}

QLabel#loginTitle {{
    font-size: 26px;
    font-weight: 700;
    color: {COLORS['text']};
}}

QLabel#loginSubtitle {{
    font-size: 14px;
    color: {COLORS['text_secondary']};
}}
"""

# Stat Card Styles
def get_stat_card_stylesheet(gradient_start, gradient_end):
    """Get stylesheet for stat card with gradient"""
    return f"""
    QGroupBox {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                    stop:0 {gradient_start}, stop:1 {gradient_end});
        color: white;
        border: none;
        border-radius: 12px;
        padding: 20px;
        font-weight: 700;
        font-size: 14px;
    }}
    
    QLabel {{
        color: white;
        background: transparent;
    }}
    """

# Gradient definitions for stat cards
STAT_GRADIENTS = {
    'purple': ('#667eea', '#764ba2'),
    'pink': ('#f093fb', '#f5576c'),
    'blue': ('#4facfe', '#00f2fe'),
    'orange': ('#fa709a', '#fee140'),
}
