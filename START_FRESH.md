# 🔄 START FROM SCRATCH GUIDE

If you need to reset and start fresh, follow these exact steps.

---

## 🗑️ Clean Start (Optional)

Only if you want to completely reset:

```powershell
# Delete these if you want fresh start:
# - backend/db.sqlite3
# - backend/media/
# - frontend-react/node_modules/
```

---

## ✅ Step-by-Step Setup (First Time)

### Step 1: Backend Setup (5 minutes)

```powershell
# Navigate to backend
cd c:\Users\91985\Desktop\FOSSE_2026\backend

# Activate virtual environment (should already exist)
.\.venv\Scripts\Activate.ps1

# If venv doesn't exist, create it:
python -m venv venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (if not exists)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_user('admin', 'admin@example.com', 'admin123');
    print('✅ Admin user created')
else:
    print('✅ Admin user already exists')
"

# Start server
python manage.py runserver
```

✅ Backend should be running at: http://localhost:8000

**Keep this terminal open!**

---

### Step 2: Web Frontend Setup (10 minutes)

**IMPORTANT: Install Node.js first!**
- Download: https://nodejs.org/
- Install LTS version
- Restart VS Code

Then:

```powershell
# Open NEW terminal (keep backend running)
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

✅ Frontend should open at: http://localhost:3000

**Keep this terminal open too!**

---

### Step 3: Desktop App (2 minutes)

```powershell
# Open NEW terminal (keep others running)
cd c:\Users\91985\Desktop\FOSSE_2026\desktop-pyqt

# Install dependencies (if needed)
pip install -r requirements.txt

# Run app
python main.py
```

✅ Desktop window should open

---

## 🧪 Quick Test

### Test 1: Backend is Working

1. Open browser: http://localhost:8000/admin/
2. Login: admin / admin123
3. Should see Django admin panel ✅

### Test 2: Web App is Working

1. Browser should auto-open at: http://localhost:3000
2. Should see login page ✅
3. Login: admin / admin123
4. Should see dashboard ✅

### Test 3: Upload CSV

1. Click "Upload CSV" tab
2. Select: `c:\Users\91985\Desktop\FOSSE_2026\sample_equipment_data.csv`
3. Click "Upload & Process"
4. Should see success message and charts ✅

### Test 4: Desktop App

1. Desktop window should be open
2. Login: admin / admin123
3. Click "Browse" → select sample CSV
4. Click "Upload & Process"
5. Should see charts ✅

---

## 🐛 Common Issues & Fixes

### Issue: "python not found"
**Fix:**
```powershell
# Use full path
C:\Users\91985\AppData\Local\Programs\Python\Python311\python.exe
```

### Issue: "npm not found"
**Fix:** Install Node.js from https://nodejs.org/ and restart VS Code

### Issue: "Module not found: django"
**Fix:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Fix:**
```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

### Issue: "CORS errors"
**Fix:** Already configured! Just make sure:
- Backend is running on port 8000
- Frontend API URL is correct in `src/services/api.js`

### Issue: "No such table: equipment_dataset"
**Fix:**
```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Invalid credentials"
**Fix:** Recreate superuser:
```powershell
cd backend
python manage.py createsuperuser
# Username: admin
# Password: admin123
```

---

## 📝 Environment Variables (Optional)

Create `.env` file in backend folder:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=db.sqlite3
```

Then update `settings.py`:
```python
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

---

## 🔧 Verify Installation

Run this to check everything:

```powershell
# Check Python
python --version
# Should show: Python 3.11.x or higher

# Check Node.js
node --version
# Should show: v18.x.x or higher

# Check npm
npm --version
# Should show: 9.x.x or higher

# Check Django
cd backend
python -c "import django; print(django.get_version())"
# Should show: 5.2.10

# Check React dependencies
cd frontend-react
npm list react
# Should show react version
```

---

## 🚀 Quick Commands Reference

### Backend Commands
```powershell
cd backend
python manage.py runserver          # Start server
python manage.py migrate             # Run migrations
python manage.py makemigrations      # Create migrations
python manage.py createsuperuser     # Create admin user
python manage.py shell               # Django shell
python manage.py test                # Run tests
```

### Frontend Commands
```powershell
cd frontend-react
npm install                          # Install dependencies
npm run dev                          # Start dev server
npm run build                        # Build for production
npm run preview                      # Preview build
```

### Desktop Commands
```powershell
cd desktop-pyqt
python main.py                       # Run desktop app
pip install -r requirements.txt     # Install dependencies
```

---

## 📦 If You Need to Reinstall Everything

### Backend
```powershell
cd backend
rmdir /s venv                        # Delete venv
python -m venv venv                  # Create new venv
.\.venv\Scripts\Activate.ps1         # Activate
pip install -r requirements.txt     # Install all
python manage.py migrate             # Setup database
```

### Frontend
```powershell
cd frontend-react
rmdir /s node_modules                # Delete node_modules
npm install                          # Fresh install
```

### Desktop
```powershell
pip install --force-reinstall PyQt5 requests matplotlib
```

---

## ✨ Production Checklist (Future)

When deploying to production:

- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use PostgreSQL instead of SQLite
- [ ] Use environment variables for secrets
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up logging
- [ ] Use Gunicorn/uWSGI
- [ ] Use Nginx reverse proxy
- [ ] Deploy to Heroku/AWS/DigitalOcean

---

## 🎯 Final Checklist Before Demo

- [ ] Backend running (port 8000)
- [ ] Frontend running (port 3000) or Node.js ready to install
- [ ] Desktop app launches
- [ ] Can login with admin/admin123
- [ ] Can upload sample CSV
- [ ] Charts display correctly
- [ ] Can download PDF
- [ ] History shows uploads
- [ ] All documentation files present

---

## 🆘 Emergency Reset

If everything is broken:

```powershell
# 1. Stop all servers (Ctrl+C in all terminals)

# 2. Reset database
cd backend
del db.sqlite3
del db.sqlite3-journal
python manage.py migrate
python manage.py createsuperuser

# 3. Clear frontend cache
cd frontend-react
rmdir /s node_modules
npm install

# 4. Restart everything
cd backend
python manage.py runserver

# In new terminal:
cd frontend-react
npm run dev

# In new terminal:
cd desktop-pyqt
python main.py
```

---

## 📞 Support Resources

**Documentation:**
- README.md - Main documentation
- QUICK_START.md - Fast setup
- ARCHITECTURE.md - Technical details

**Official Docs:**
- Django: https://docs.djangoproject.com/
- React: https://react.dev/
- PyQt5: https://doc.qt.io/qtforpython/

**Stack Overflow:**
- Tag: [django]
- Tag: [reactjs]
- Tag: [pyqt5]

---

## ✅ You're All Set!

Follow these steps in order, and you'll have a working project in 15-20 minutes.

**Remember:** 
- Keep backend running always
- Frontend needs Node.js
- Desktop works independently

**Good luck! 🚀**
