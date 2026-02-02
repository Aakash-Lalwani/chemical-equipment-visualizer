"""
Matplotlib Style Configuration

Ensures Matplotlib charts in desktop app match web charts exactly
"""

import matplotlib.pyplot as plt
from .style_tokens import CHART_COLORS, TEXT_PRIMARY, BG_WHITE, BORDER

def apply_chart_style():
    """
    Apply consistent chart styling to all Matplotlib plots
    
    Call this once at app startup:
        from ui.mpl_style import apply_chart_style
        apply_chart_style()
    """
    plt.rcParams.update({
        # Figure
        'figure.facecolor': BG_WHITE,
        'figure.edgecolor': BORDER,
        'figure.figsize': (10, 6),
        'figure.dpi': 100,
        
        # Axes
        'axes.facecolor': BG_WHITE,
        'axes.edgecolor': BORDER,
        'axes.labelcolor': TEXT_PRIMARY,
        'axes.titlecolor': TEXT_PRIMARY,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'axes.linewidth': 1.5,
        'axes.grid': True,
        'axes.prop_cycle': plt.cycler(color=CHART_COLORS),
        
        # Grid
        'grid.color': BORDER,
        'grid.linestyle': '--',
        'grid.linewidth': 0.8,
        'grid.alpha': 0.3,
        
        # Ticks
        'xtick.color': TEXT_PRIMARY,
        'ytick.color': TEXT_PRIMARY,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        
        # Legend
        'legend.facecolor': BG_WHITE,
        'legend.edgecolor': BORDER,
        'legend.framealpha': 0.95,
        'legend.fontsize': 10,
        
        # Lines
        'lines.linewidth': 2.5,
        'lines.markersize': 8,
        
        # Font
        'font.family': 'sans-serif',
        'font.sans-serif': ['Segoe UI', 'Arial', 'DejaVu Sans'],
        'font.size': 11,
    })

def get_chart_color(index):
    """
    Get chart color by index
    
    Args:
        index: Color index (0-7)
    
    Returns:
        Hex color string
    """
    return CHART_COLORS[index % len(CHART_COLORS)]
