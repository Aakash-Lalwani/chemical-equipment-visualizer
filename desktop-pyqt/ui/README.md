# UI Components Module

This directory contains reusable UI components and design tokens for the desktop application.

## Structure

- **`style_tokens.py`** - Color palette, spacing, typography constants  
  Single source of truth for design values. Import these instead of hard-coding hex colors.

- **`modern_login.qss`** - Qt Stylesheet for login window  
  Clean, professional styling without gradient artifacts.

- **`login_widget.py`** - ModernLoginWidget class  
  Improved login screen with centered card layout and clear visual feedback.

- **`mpl_style.py`** - Matplotlib configuration  
  Ensures charts match web app colors exactly.

## Usage

### Using Style Tokens

```python
from ui.style_tokens import PRIMARY, SPACING_MD, TEXT_PRIMARY

# Use in QSS
button_style = f"background-color: {PRIMARY}; padding: {SPACING_MD}px;"

# Use in Python logic
if valid:
    label.setStyleSheet(f"color: {SUCCESS};")
```

### Using ModernLoginWidget

```python
from ui.login_widget import ModernLoginWidget

# Option 1: Replace existing login
login_widget = ModernLoginWidget(api_url="http://127.0.0.1:8000")
login_widget.loginSuccess.connect(self.on_login_success)

# Option 2: Keep existing LoginWindow (gradual migration)
# Just import for future use
```

### Applying Matplotlib Style

```python
from ui.mpl_style import apply_chart_style

# Call once at app startup (in main.py)
apply_chart_style()

# Charts will now use consistent colors
```

## Benefits

✅ **Consistency** - Desktop and web share exact color palette  
✅ **Maintainability** - Change one value, updates everywhere  
✅ **Clean Code** - No magic hex values scattered in code  
✅ **Professional** - Modern design without visual artifacts

## Color Palette

All colors match `frontend-react/src/styles/global.css`:

- Primary: `#2563eb` (blue)
- Success: `#10b981` (green)
- Danger: `#ef4444` (red)
- Warning: `#f59e0b` (amber)

See `style_tokens.py` for complete palette.
