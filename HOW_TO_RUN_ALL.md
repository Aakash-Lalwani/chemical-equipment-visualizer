# 🚀 RUN EVERYTHING AT ONCE

## ⚡ QUICK START (1-Click Launch)

### Windows PowerShell Method (Recommended)
```powershell
# Right-click and "Run with PowerShell"
RUN_ALL.ps1
```

OR

### Batch File Method (Simpler)
```batch
# Double-click this file
RUN_ALL.bat
```

---

## 🎯 WHAT HAPPENS

When you run the launcher:

### 1️⃣ Backend Server Starts
- New window opens: **"BACKEND - Django Server"**
- Runs on: http://127.0.0.1:8000
- Keep this window OPEN!

### 2️⃣ Frontend Server Starts (if Node.js installed)
- New window opens: **"FRONTEND - React Dev Server"**
- Runs on: http://localhost:3000
- Takes 10-15 seconds to start
- Keep this window OPEN!

### 3️⃣ Desktop App Launches
- New window opens: **"DESKTOP - PyQt5 App"**
- GUI application window appears
- Keep this window OPEN!

### 4️⃣ Browser Opens Automatically
- Opens http://localhost:3000 (or admin page if no Node.js)
- Wait a few seconds for everything to load

---

## 🪟 YOU WILL SEE

After running the launcher, you'll have **4 windows**:

```
┌─────────────────────────────────────┐
│ 1. BACKEND Terminal                 │
│    "Django version 5.2.10..."       │
│    "Starting development server..." │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 2. FRONTEND Terminal (if Node.js)   │
│    "VITE ready in 250ms..."         │
│    "Local: http://localhost:3000/"  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 3. DESKTOP App Terminal              │
│    Shows any console output         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 4. DESKTOP App GUI Window           │
│    Login screen with tabs           │
└─────────────────────────────────────┘
```

---

## 🌐 ACCESS YOUR APPLICATIONS

### Web Frontend (React)
- **URL:** http://localhost:3000
- **Login:** admin / admin123
- **Features:** Beautiful charts, drag-drop upload, responsive design

### Desktop App (PyQt5)
- **Window:** Opens automatically
- **Login:** admin / admin123
- **Features:** Native GUI, Matplotlib charts, file dialogs

### Backend Admin
- **URL:** http://127.0.0.1:8000/admin
- **Login:** admin / admin123
- **Features:** Database management, user admin

---

## 📊 TESTING THE PROJECT

### Step 1: Login
- Use credentials: **admin** / **admin123**
- Works in both web and desktop apps

### Step 2: Upload CSV
- Click "Upload" tab
- Choose file: **sample_equipment_data.csv** (in project root)
- Click upload button

### Step 3: View Results
- See statistics dashboard
- View bar charts and pie charts
- Check data table

### Step 4: Download PDF
- Click "Download PDF Report" button
- PDF file saves automatically

---

## 🛑 STOPPING EVERYTHING

### Method 1: Close All Windows
- Close each terminal window
- Close the desktop app GUI window

### Method 2: Ctrl+C in Each Terminal
- Press Ctrl+C in backend terminal
- Press Ctrl+C in frontend terminal (if running)
- Close desktop app window

### Method 3: Task Manager (if stuck)
- Open Task Manager (Ctrl+Shift+Esc)
- Find Python/Node processes
- End tasks

---

## ⚠️ TROUBLESHOOTING

### "Port 8000 already in use"
**Problem:** Backend already running
**Solution:**
```bash
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### "Node.js not found"
**Problem:** React frontend won't start
**Solution:**
1. Install Node.js from https://nodejs.org/
2. Restart computer
3. Run RUN_ALL.bat again

### "npm: command not found"
**Problem:** Node.js not in PATH
**Solution:**
1. Restart terminal after installing Node.js
2. Or restart computer

### "Desktop app doesn't open"
**Problem:** PyQt5 might have errors
**Solution:**
1. Check the desktop app terminal for errors
2. Ensure virtual environment is activated
3. Try running manually: `cd desktop-pyqt && python main.py`

### "Frontend takes too long"
**Problem:** First-time npm install is slow
**Solution:**
- Wait 2-3 minutes for first run
- Check frontend terminal for progress
- Subsequent runs will be fast

---

## 📁 MANUAL START (If Launcher Fails)

### Terminal 1: Backend
```bash
cd c:\Users\91985\Desktop\FOSSE_2026\backend
python manage.py runserver
```

### Terminal 2: Frontend (requires Node.js)
```bash
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react
npm install  # First time only
npm run dev
```

### Terminal 3: Desktop
```bash
cd c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt
python main.py
```

---

## ✅ SUCCESS INDICATORS

You know everything is working when:

- ✅ Backend terminal shows: "Starting development server at http://127.0.0.1:8000/"
- ✅ Frontend terminal shows: "Local: http://localhost:3000/"
- ✅ Desktop app window opens with login screen
- ✅ Browser opens and shows the login page
- ✅ You can login with admin/admin123
- ✅ You can upload CSV files
- ✅ Charts display correctly
- ✅ PDF downloads work

---

## 🎓 WHAT EACH COMPONENT DOES

### 🔴 Backend (Django)
- **Purpose:** REST API server
- **Port:** 8000
- **Functions:**
  - User authentication
  - CSV file processing
  - Database storage
  - PDF generation
  - API endpoints

### 🔵 Frontend (React)
- **Purpose:** Web user interface
- **Port:** 3000
- **Functions:**
  - Modern, responsive design
  - Interactive charts (Chart.js)
  - File upload with drag-drop
  - Real-time data visualization
  - Dashboard and history views

### 🟢 Desktop (PyQt5)
- **Purpose:** Native Windows application
- **Port:** None (standalone GUI)
- **Functions:**
  - Native window interface
  - Matplotlib chart integration
  - File browser dialogs
  - Offline-capable UI
  - All features of web app

---

## 💡 TIPS

1. **Keep terminals open** - Don't close them while using the app
2. **Wait for startup** - Frontend takes 10-15 seconds first time
3. **Use sample data** - sample_equipment_data.csv is ready to test
4. **Check terminal logs** - Errors appear in terminal windows
5. **Admin panel** - Use Django admin for database inspection

---

## 🎯 PROJECT READY!

Your complete full-stack project is now running with:
- ✅ Django REST API backend
- ✅ React web frontend
- ✅ PyQt5 desktop application
- ✅ All features working
- ✅ Sample data ready

**Just double-click `RUN_ALL.bat` and everything starts!**

---

## 📞 HELP

If something doesn't work:
1. Check [DEBUG_REPORT.md](DEBUG_REPORT.md) for common issues
2. Check [QUICK_START.md](QUICK_START.md) for setup steps
3. Check [API_TESTING.md](API_TESTING.md) for endpoint testing
4. Check terminal windows for error messages

---

**Happy Testing! 🚀**
