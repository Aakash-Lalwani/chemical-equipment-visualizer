/**
 * Design Tokens for React Components
 * 
 * Shared color palette - matches desktop-pyqt/ui/style_tokens.py
 * Import these instead of hard-coding colors
 */

export const colors = {
  // Primary Colors
  primary: '#2563eb',
  primaryDark: '#1e40af',
  primaryLight: '#3b82f6',
  
  // Status Colors
  success: '#10b981',
  danger: '#ef4444',
  warning: '#f59e0b',
  info: '#3b82f6',
  
  // Neutral Colors
  bgPrimary: '#f9fafb',
  bgSecondary: '#f3f4f6',
  bgWhite: '#ffffff',
  border: '#e5e7eb',
  
  // Text Colors
  textPrimary: '#1f2937',
  textSecondary: '#6b7280',
  textLight: '#9ca3af',
  
  // Chart Colors (for Chart.js consistency)
  chartColors: [
    '#3b82f6',  // Blue
    '#10b981',  // Green
    '#8b5cf6',  // Purple
    '#f59e0b',  // Orange
    '#ef4444',  // Red
    '#06b6d4',  // Cyan
    '#ec4899',  // Pink
    '#84cc16',  // Lime
  ],
};

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
};

export const radius = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  full: '9999px',
};

export const fontSize = {
  xs: '12px',
  sm: '14px',
  base: '16px',
  lg: '18px',
  xl: '24px',
  '2xl': '32px',
};

// Helper: Get chart color by index
export const getChartColor = (index) => {
  return colors.chartColors[index % colors.chartColors.length];
};
