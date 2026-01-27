# Quick Start Guide

## 🚀 Get Your Project Running in 5 Minutes

### Step 1: Start the Backend (Django)

Open Terminal in VS Code and run:

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\backend
python manage.py runserver
```

✅ Backend should be running at: `http://localhost:8000`

Leave this terminal running!

---

### Step 2: Start the Web Frontend (React)

**First time only - Install Node.js:**
1. Download from: https://nodejs.org/
2. Install and restart VS Code

**Then run:**

Open a NEW terminal (keep the first one running) and run:

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react
npm install
npm run dev
```

✅ Frontend should open at: `http://localhost:3000`

---

### Step 3: Login

Use these credentials:
- **Username:** admin
- **Password:** admin123

---

### Step 4: Upload CSV

1. Click "Browse" or use the file input
2. Select `sample_equipment_data.csv` from the project root
3. Click "Upload & Process"
4. View your dashboard with charts!

---

### Step 5: Run Desktop App (Optional)

Open a NEW terminal and run:

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt
python main.py
```

Login with the same credentials!

---

## 🎯 What Should Work

✅ Login/Register  
✅ CSV Upload  
✅ Dashboard with charts  
✅ Data table  
✅ Upload history  
✅ PDF download  
✅ Desktop app with all features  

---

## ❌ Common Errors & Fixes

### "ModuleNotFoundError: No module named 'django'"
**Fix:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "npm is not recognized"
**Fix:** Install Node.js from https://nodejs.org/ and restart VS Code

### "Connection refused" or "Network Error"
**Fix:** Make sure Django backend is running on port 8000

### Port 8000 already in use
**Fix:** 
```powershell
python manage.py runserver 8001
```
Then update API_BASE_URL in:
- `frontend-react/src/services/api.js`
- `desktop-pyqt/main.py`

---

## 🎓 Project Demo Flow

1. **Login** → Show authentication works
2. **Upload CSV** → Show file processing
3. **View Dashboard** → Show charts and statistics
4. **Check History** → Show last 5 datasets
5. **Download PDF** → Show report generation
6. **Show Desktop App** → Same features, different interface

---

## 📝 Interview Questions You Should Prepare

1. **Why did you choose Django?**
   - Built-in admin, ORM, security features
   - Perfect for REST APIs with DRF
   - Rapid development

2. **Explain the data flow:**
   - User uploads CSV
   - Backend validates and processes with Pandas
   - Calculates statistics
   - Stores in SQLite
   - Returns JSON to frontend
   - Frontend displays with Chart.js

3. **How does authentication work?**
   - Token-based auth
   - User logs in → gets token
   - Token stored in localStorage
   - Sent with each API request

4. **What is the 5-dataset limit feature?**
   - After each upload, check total datasets
   - If > 5, delete oldest ones
   - Prevents database bloat

5. **How are PDFs generated?**
   - ReportLab library
   - Creates PDF in memory
   - Adds tables, charts, text
   - Returns as downloadable file

---

## ✨ Tips for Presentation

1. **Have everything running before demo**
2. **Use the sample CSV file** (it's guaranteed to work)
3. **Show both web and desktop apps**
4. **Explain the tech stack** (Django, React, PyQt5)
5. **Mention scalability** (can handle more data, add features)

---

**You're ready to present! 🎉**
