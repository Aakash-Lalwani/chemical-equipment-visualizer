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

Open PowerShell:

```powershell
pip install pyinstaller
```

**Verify installation:**
```powershell
pyinstaller --version
```

Expected output: `6.x.x` or similar

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

### Create User README:

The README.txt is already in the distribution folder with:
- Quick start instructions
- System requirements
- Configuration guide
- Troubleshooting tips
- Feature list

---

## 🎓 ACADEMIC SUBMISSION NOTES

### What to Tell Your Evaluator:

**About PyInstaller:**
"The desktop application is packaged using PyInstaller, which bundles the Python interpreter and all dependencies into a single executable. This allows distribution to end-users without requiring Python installation, improving accessibility and user experience."

**About Architecture:**
"The desktop application follows a client-server architecture, communicating with the Django backend via RESTful API endpoints. This separation of concerns allows for independent scaling and deployment of frontend and backend components."

**About Configuration:**
"The application uses an external configuration file (config.ini) for backend URL management, allowing system administrators to point the application to different backend servers without recompilation. This demonstrates good software engineering practices for maintainability."

**About Security:**
"Token-based authentication ensures secure API communication. Credentials are transmitted over HTTPS to the production backend, protecting user data during transit."

**About File Size:**
"The executable size (~150-250 MB) is due to bundling the Python interpreter, PyQt5 GUI framework, and Matplotlib visualization library. This trade-off prioritizes ease of distribution over file size, which is acceptable for modern systems with adequate storage."

---

## ⚠️ COMMON BUILD ERRORS

### Error: "Module not found: matplotlib.backends.backend_qt5agg"

**Fix:** Add to `hiddenimports` in spec file:
```python
hiddenimports=[
    'matplotlib.backends.backend_qt5agg',  # Add this
]
```

Rebuild:
```powershell
pyinstaller equipment_visualizer.spec --clean
```

### Error: "Cannot find config.ini"

**Fix:** Ensure `datas` in spec file includes:
```python
datas=[('config.ini', '.')],
```

### Error: "The file is not a valid Win32 application"

**Fix:** You're trying to run on wrong architecture (32-bit vs 64-bit)

Rebuild for correct architecture:
```powershell
pyinstaller equipment_visualizer.spec --clean
```

### Error: Windows Defender blocks .exe

**This is NORMAL for unsigned executables!**

**Why it happens:** Your .exe isn't digitally signed (costs money)

**User solution:**
1. Windows Defender shows warning
2. Click "More info"
3. Click "Run anyway"

**For academic submission:** Mention that production apps should be code-signed for $200-300/year.

---

## 🔒 STEP 9: Create Installer (Optional Advanced)

Want to create a professional installer like "Setup.exe"?

### Option 1: Inno Setup (Free, Recommended)

Download: https://jrsoftware.org/isdl.php

**Inno Setup Script Example:**
```
[Setup]
AppName=Equipment Visualizer
AppVersion=1.0
DefaultDirName={pf}\EquipmentVisualizer
DefaultGroupName=Equipment Visualizer
OutputDir=installer

[Files]
Source: "dist\EquipmentVisualizer.exe"; DestDir: "{app}"
Source: "config.ini"; DestDir: "{app}"
Source: "sample_equipment_data.csv"; DestDir: "{app}"

[Icons]
Name: "{group}\Equipment Visualizer"; Filename: "{app}\EquipmentVisualizer.exe"
Name: "{commondesktop}\Equipment Visualizer"; Filename: "{app}\EquipmentVisualizer.exe"
```

**Result:** Creates `EquipmentVisualizer_Setup.exe`

### Option 2: Just use ZIP (Simplest)

For academic submission, a ZIP file is perfectly acceptable!

```powershell
Compress-Archive -Path EquipmentVisualizer_Distribution\* -DestinationPath EquipmentVisualizer_v1.0.zip
```

---

## 📊 STEP 10: Share/Submit Your .exe

### Option 1: Google Drive

```powershell
# Zip the distribution folder
Compress-Archive -Path EquipmentVisualizer_Distribution\* -DestinationPath EquipmentVisualizer.zip
```

Upload `EquipmentVisualizer.zip` to Google Drive and share link.

### Option 2: GitHub Releases

```powershell
# Create release
gh release create v1.0.0 EquipmentVisualizer.zip
```

### Option 3: Direct File Transfer

Copy `EquipmentVisualizer_Distribution` folder to USB drive.

---

## ✅ PHASE 3 CHECKLIST

Before moving to Phase 4:

- [ ] PyInstaller installed
- [ ] config.ini updated with Railway URL
- [ ] .exe built successfully
- [ ] .exe runs and opens application window
- [ ] Login works with deployed backend
- [ ] CSV upload works
- [ ] Charts display correctly
- [ ] PDF export works
- [ ] Distribution folder created with:
  - [ ] EquipmentVisualizer.exe
  - [ ] config.ini
  - [ ] sample_equipment_data.csv
  - [ ] README.txt
- [ ] .exe tested on clean Windows machine (optional but recommended)

---

## 🧪 TESTING ON ANOTHER COMPUTER

**Best practice:** Test on a computer without Python installed!

### Steps:

1. Copy `EquipmentVisualizer_Distribution` folder to USB drive
2. Plug into another Windows computer
3. Double-click `EquipmentVisualizer.exe`
4. Test full workflow

**Why?** Ensures .exe is truly standalone and doesn't rely on your development environment.

---

## 📝 DISTRIBUTION FOLDER STRUCTURE

Final structure:
```
EquipmentVisualizer_Distribution/
├── EquipmentVisualizer.exe     (150-250 MB)
├── config.ini                   (Configuration)
├── sample_equipment_data.csv    (Test data)
└── README.txt                   (User instructions)
```

**Total size:** ~150-250 MB

**Compressed (ZIP):** ~60-100 MB

---

## 🎉 PHASE 3 COMPLETE!

Your desktop application is now:
- ✅ Packaged as standalone .exe
- ✅ Configurable via config.ini
- ✅ Ready for distribution
- ✅ No Python installation required
- ✅ Connected to deployed Railway backend
- ✅ Professional README included

**Next:** PHASE 4 - Final Polish & Documentation

---

**Ready to proceed to Phase 4?**
