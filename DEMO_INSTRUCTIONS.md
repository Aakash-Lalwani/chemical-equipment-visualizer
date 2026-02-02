# Demo Video Instructions (2-3 Minutes)

## Pre-Recording Checklist

### Setup (5 minutes before recording)
- [ ] Close all unnecessary applications and browser tabs
- [ ] Clear browser cookies/cache for clean login demo
- [ ] Prepare `sample_equipment_data.csv` on Desktop for easy access
- [ ] Test screen recording software (OBS, Camtasia, etc.)
- [ ] Set screen resolution to 1920x1080 for clarity
- [ ] Close notification panels (email, Slack, etc.)

### Services to Start
```powershell
# Option 1: Use the automated launcher
cd c:\Users\91985\Desktop\FOSSE_2026
.\RUN_ALL.bat

# Option 2: Start manually (if you want more control)
# Terminal 1 - Backend
cd c:\Users\91985\Desktop\FOSSE_2026\backend
.venv\Scripts\activate
python manage.py runserver

# Terminal 2 - Frontend (optional)
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react
npm run dev
```

### Verify Services Running
- [ ] Backend: http://127.0.0.1:8000/admin (should show Django admin login)
- [ ] Frontend: http://localhost:3000 (should show login page)
- [ ] Desktop app ready to launch (don't start yet)

---

## Recording Timeline (Exactly 2:30 - 3:00 minutes)

### **[0:00-0:20] Introduction** (20 seconds)
**What to show:**
- [ ] VS Code with project folder open
- [ ] Briefly show folder structure in sidebar

**What to say:**
> "This is the Chemical Equipment Parameter Visualizer - a full-stack application built with Django REST Framework, React, and PyQt5. It allows users to upload CSV files with equipment data and generates comprehensive analytics and visualizations."

---

### **[0:20-0:30] Backend Overview** (10 seconds)
**What to show:**
- [ ] Switch to browser at `http://127.0.0.1:8000/admin`
- [ ] Show Django admin login page

**What to say:**
> "The backend is built with Django and provides a RESTful API with token-based authentication."

---

### **[0:30-1:30] Web Application Demo** (60 seconds)
**What to show:**
1. **Login** (0:30-0:40)
   - [ ] Navigate to `http://localhost:3000`
   - [ ] Login with: `admin` / `admin123`
   - [ ] Show successful login redirect

2. **CSV Upload** (0:40-1:00)
   - [ ] Click "Upload CSV" tab
   - [ ] Drag and drop `sample_equipment_data.csv` OR click to browse
   - [ ] Show upload progress
   - [ ] Show success message with summary

3. **Dashboard View** (1:00-1:30)
   - [ ] Navigate to Dashboard tab
   - [ ] Point out key metrics:
     - Total Equipment: **10**
     - Average Flowrate: **~195.23**
     - Average Pressure: **~2.46**
     - Average Temperature: **~83.33**
   - [ ] Show Bar Chart (equipment type distribution)
   - [ ] Show Pie Chart

**What to say:**
> "After logging in, I'll upload the sample CSV file. The system validates the data, calculates summary statistics, and displays them on the dashboard. Here we can see 10 equipment items with averages for flowrate, pressure, and temperature. The charts show the distribution across different equipment types."

---

### **[1:30-2:00] History & PDF Export** (30 seconds)
**What to show:**
1. **History Tab** (1:30-1:45)
   - [ ] Navigate to History tab
   - [ ] Show list of uploaded datasets
   - [ ] Highlight upload timestamp and statistics

2. **PDF Download** (1:45-2:00)
   - [ ] Click "Download PDF" button on latest upload
   - [ ] Show PDF opening in viewer
   - [ ] Briefly scroll through PDF showing:
     - Dataset info table
     - Summary statistics
     - Equipment type chart

**What to say:**
> "The History page keeps track of the last 5 uploads per user. Each upload has a summary and can be exported as a PDF report containing all charts and statistics."

---

### **[2:00-2:40] Desktop Application** (40 seconds)
**What to show:**
1. **Launch** (2:00-2:10)
   - [ ] Launch PyQt5 desktop app
   - [ ] Show login dialog
   - [ ] Login with same credentials

2. **Desktop Features** (2:10-2:40)
   - [ ] Show main window with tabs
   - [ ] Navigate to History tab
   - [ ] Click on a dataset to view details
   - [ ] Show Matplotlib charts (bar chart, pie chart)
   - [ ] Point out native desktop UI elements

**What to say:**
> "The desktop application provides the same functionality as the web app but with a native PyQt5 interface. Users can view their upload history and visualizations using Matplotlib charts, perfect for offline use or users who prefer desktop applications."

---

### **[2:40-3:00] Code Highlight & Conclusion** (20 seconds)
**What to show:**
- [ ] Quick switch back to VS Code
- [ ] Show one or two key files (e.g., `backend/equipment/views.py` or `utils.py`)
- [ ] Briefly mention features

**What to say:**
> "Key features include CSV validation with Pandas, automatic data cleanup keeping only the last 5 uploads, and accessibility compliance with WCAG 2.1 AA standards. The entire project is well-documented with clear setup instructions and ready for deployment. Thank you!"

---

## Post-Recording Checklist

### Video Editing Tips
- [ ] Trim any dead air at beginning/end
- [ ] Add title card (optional): "Chemical Equipment Parameter Visualizer"
- [ ] Add your name and date
- [ ] Check audio levels (should be clear and not too quiet)
- [ ] Export in 1080p MP4 format

### Final Checks Before Submission
- [ ] Video length is between 2:30 and 3:00 minutes
- [ ] All required features are demonstrated
- [ ] Audio is clear and understandable
- [ ] Screen content is readable (text not too small)
- [ ] No sensitive information visible (passwords hidden by dots)

---

## Troubleshooting

### Common Issues During Recording

**Backend not responding:**
```powershell
# Check if backend is running
netstat -ano | findstr :8000

# Restart backend
cd backend
.venv\Scripts\activate
python manage.py runserver
```

**Frontend not loading:**
```powershell
# Check if frontend is running
netstat -ano | findstr :3000

# Restart frontend
cd frontend-react
npm run dev
```

**Desktop app crashes on startup:**
- Check config.ini has correct backend URL
- Ensure backend is running first
- Check Python version (needs 3.10+)

**CSV upload fails:**
- Verify sample_equipment_data.csv has correct headers
- Check file size is under 10MB
- Ensure backend has write permissions to media/datasets/

---

## Quick Reference: Demo Data

**Sample CSV Stats (for verification):**
- Total Equipment: 10
- Average Flowrate: 195.23
- Average Pressure: 2.46
- Average Temperature: 83.33
- Equipment Types:
  - Reactor: 2
  - Heat Exchanger: 2
  - Pump: 2
  - Column: 1
  - Compressor: 1
  - Mixer: 1
  - Separator: 1

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

**URLs:**
- Backend Admin: http://127.0.0.1:8000/admin
- Backend API: http://127.0.0.1:8000/api
- Frontend: http://localhost:3000 (or http://localhost:5173 with Vite)

---

Good luck with your demo! 🎬
