# 🖥️ DESKTOP APP PACKAGING GUIDE - PyInstaller

## 📋 WHAT WE JUST DID (Preparation)

### Files Modified/Created:
1. ✅ **main.py** - Added config.ini support and configparser import
2. ✅ **config.ini** - Configuration file for backend URL
3. ✅ **equipment_visualizer.spec** - PyInstaller build configuration

---

## 🎯 STEP 1: Understanding PyInstaller (ELI5)

### **What is PyInstaller?**

**ELI5:** PyInstaller turns your Python code into a `.exe` file that runs on any Windows computer without needing Python installed.

**Analogy:**
- **Your Python code** = Recipe (needs kitchen/Python to cook)
- **PyInstaller** = Pre-cooked frozen meal (microwave/run anywhere)
- **.exe file** = Ready-to-eat (no kitchen needed)

### **How PyInstaller Works:**

1. **Analyzes** your Python code
2. **Finds** all dependencies (PyQt5, requests, matplotlib, etc.)
3. **Bundles** everything into one `.exe` file
4. **Includes** Python interpreter inside the .exe

**Result:** User double-clicks `.exe` → app runs immediately!

---

## 📝 STEP 2: Understanding the Code Changes

### **main.py Changes**

#### Added Import:
```python
import configparser
```

**What:** Library for reading `.ini` configuration files  
**Why:** Allows loading backend URL from config.ini  
**ELI5:** "Tool for reading settings files"

#### Added Config Loading Function:
```python
def load_config():
    """Load configuration from config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    
    if os.path.exists(config_path):
        config.read(config_path)
        return config.get('API', 'backend_url', fallback='http://localhost:8000/api')
    else:
        return os.environ.get('BACKEND_URL', 'http://localhost:8000/api')

API_BASE_URL = load_config()
```

**Breaking it down:**
- `config_path = os.path.join(...)` - Find config.ini next to main.py
- `if os.path.exists(config_path)` - Check if config.ini exists
- `config.read(config_path)` - Read the file
- `config.get('API', 'backend_url', ...)` - Get backend_url from [API] section
- `fallback='http://localhost:8000/api'` - Use localhost if not found
- `else: return os.environ.get(...)` - Alternative: environment variable

**ELI5:** "Check config file for backend URL, otherwise use localhost"

**Why this matters for .exe:**
- Users can edit `config.ini` without recompiling
- Easy to switch between local testing and production
- No need to rebuild .exe for different backends

---

### **config.ini Explained**

```ini
[API]
# Backend URL Configuration
# For local development: http://localhost:8000/api
# For production: https://your-railway-backend.up.railway.app/api

backend_url = https://your-railway-backend.up.railway.app/api

[App]
app_name = Chemical Equipment Visualizer
version = 1.0.0
```

**Structure:**
- `[API]` - Section name
- `backend_url = ...` - Key-value pair
- Lines starting with `#` - Comments (ignored)

**ELI5:** "Settings file that users can edit with Notepad"

**How it works:**
- User wants to test locally → change to `http://localhost:8000/api`
- User wants production → change to Railway URL
- No coding required!

---

### **equipment_visualizer.spec Explained**

This file tells PyInstaller HOW to build your .exe.

#### Key Sections:

**1. Analysis Section:**
```python
a = Analysis(
    ['main.py'],                  # Main Python file to build from
    datas=[('config.ini', '.')],  # Include config.ini in .exe
    hiddenimports=[               # Force include these packages
        'matplotlib.backends.backend_qt5agg',
        'PyQt5',
        'requests',
        'configparser',
    ],
)
```

**What this does:**
- `['main.py']` - Start building from main.py
- `datas=[('config.ini', '.')]` - Include config.ini in the .exe
  - **Format:** `(source_file, destination_folder)`
  - `.` means root of .exe folder
- `hiddenimports=[]` - Packages PyInstaller might miss automatically

**ELI5:** "Tell PyInstaller what to pack into the suitcase (.exe)"

**2. EXE Section:**
```python
exe = EXE(
    name='EquipmentVisualizer',   # Name of .exe file
    console=False,                # Don't show black console window
    upx=True,                     # Compress for smaller size
    icon='icon.ico'               # Application icon (optional)
)
```

**What this does:**
- `name='EquipmentVisualizer'` - Creates `EquipmentVisualizer.exe`
- `console=False` - No black command window (cleaner UI)
- `upx=True` - Compress to reduce file size
- `icon='icon.ico'` - Custom icon (we'll create this)

**ELI5:** "Customize how the .exe looks and behaves"

---

## 🚀 STEP 3: Install PyInstaller

Open PowerShell as Administrator:

```powershell
pip install pyinstaller
```

**Verify installation:**
```powershell
pyinstaller --version
```

Expected output: `6.x.x` or similar

**Why Administrator?** PyInstaller needs to create files in system directories.

---

## 🎨 STEP 4: Create Application Icon (Optional but Professional)

### Option 1: Use Existing Icon

If you have a `.png` logo:

```powershell
# Install pillow for image conversion
pip install pillow

# Convert PNG to ICO
python -c "from PIL import Image; img = Image.open('logo.png'); img.save('icon.ico')"
```

### Option 2: Use Online Converter

1. Go to https://convertio.co/png-ico/
2. Upload your logo PNG
3. Download `icon.ico`
4. Move to `desktop-pyqt` folder

### Option 3: Skip for Now

If no icon, remove this line from `equipment_visualizer.spec`:
```python
icon='icon.ico'
```

**For academic submission:** Icon is optional but looks more professional!

---

## 🛠️ STEP 5: Update config.ini with Railway URL

**CRITICAL:** Before building .exe, update config.ini!

Open `config.ini` and replace:
```ini
backend_url = https://your-railway-backend.up.railway.app/api
```

With your ACTUAL Railway URL:
```ini
backend_url = https://equipment-backend-production-abc123.up.railway.app/api
```

**How to find your Railway URL:**
```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\backend
railway domain
```

Copy the URL and add `/api` at the end.

---

## 🏗️ STEP 6: Build the .exe

### Navigate to desktop-pyqt folder:

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt
```

### Build using spec file:

```powershell
pyinstaller equipment_visualizer.spec --clean
```

**What --clean does:** Removes old build files (ensures fresh build)

**What happens next:**

PyInstaller will:
1. **Analyze** main.py and dependencies (~30 seconds)
2. **Collect** all required files (~1 minute)
3. **Build** the executable (~1-2 minutes)
4. **Create** `dist` folder with your .exe

**Output:**
```
Building EXE from EXE-00.toc completed successfully.
```

**Total time:** ~3-5 minutes (depending on computer speed)

### Check the result:

```powershell
dir dist
```

You should see:
```
EquipmentVisualizer.exe  (~150-250 MB)
```

**Why so large?** The .exe includes:
- Python interpreter
- PyQt5 libraries
- Matplotlib
- All dependencies

**This is NORMAL!**

---

## 🧪 STEP 7: Test the .exe

### Test 1: Run the .exe

Navigate to dist folder:
```powershell
cd dist
```

Run the executable:
```powershell
.\EquipmentVisualizer.exe
```

**Expected:** Application window opens!

### Test 2: Test Login

1. Enter credentials: admin / admin123
2. Click Login
3. **Expected:** Successfully login

**If error:** Check config.ini has correct Railway URL

### Test 3: Test CSV Upload

1. Login
2. Go to Upload tab
3. Select CSV file
4. Upload

**Expected:** Success message

### Test 4: Test Charts

1. Go to Dashboard tab
2. Select dataset
3. **Expected:** Charts render

### Test 5: Test PDF Export

1. Select dataset
2. Click "Export PDF"
3. **Expected:** PDF generated and opened

---

## 📦 STEP 8: Package for Distribution

### Create Distribution Folder

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026
mkdir EquipmentVisualizer_Distribution
```

### Copy Files:

```powershell
# Copy the .exe
copy desktop-pyqt\dist\EquipmentVisualizer.exe EquipmentVisualizer_Distribution\

# Copy config.ini (so users can edit backend URL)
copy desktop-pyqt\config.ini EquipmentVisualizer_Distribution\

# Copy sample data
copy sample_equipment_data.csv EquipmentVisualizer_Distribution\
```

### Create README for users:

```powershell
cd EquipmentVisualizer_Distribution
```

Create `README.txt`:

<function_calls>
<invoke name="create_file">
<parameter name="content">===============================================
Chemical Equipment Visualizer - Desktop App
===============================================

Version: 1.0.0

QUICK START:
1. Double-click "EquipmentVisualizer.exe"
2. Login with credentials:
   Username: admin
   Password: admin123
3. Upload "sample_equipment_data.csv" to test

SYSTEM REQUIREMENTS:
- Windows 10 or later (64-bit)
- No Python installation required!
- Internet connection (for API calls)

CONFIGURATION:
- Edit "config.ini" to change backend URL
- Default: Points to production server
- For local testing: Change to http://localhost:8000/api

TROUBLESHOOTING:

Problem: "Cannot connect to server"
Solution: Check internet connection and config.ini backend URL

Problem: "Login failed"
Solution: Verify credentials (admin / admin123)

Problem: Windows Defender blocks .exe
Solution: Click "More info" → "Run anyway" (app is safe, just unsigned)

FEATURES:
✓ Login with authentication
✓ Upload CSV datasets
✓ Visualize equipment parameters
✓ Interactive charts and statistics
✓ Export to PDF
✓ View upload history

CONTACT:
For support or questions about this application,
contact your project administrator.

Created as part of FOSSE Project 2026
