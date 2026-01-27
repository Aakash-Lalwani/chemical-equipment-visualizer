# 🚀 FRONTEND DEPLOYMENT GUIDE - Vercel

## 📋 WHAT WE JUST DID (Preparation)

### Files Modified/Created:
1. ✅ **api.js** - Dynamic API URL configuration
2. ✅ **.env.local** - Local development variables
3. ✅ **.env.production** - Production variables
4. ✅ **vercel.json** - Vercel configuration
5. ✅ **.gitignore** - Exclude sensitive files

---

## 🎯 STEP 1: Understanding the Changes

### **api.js Changes Explained (ELI5)**

#### Before:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

**Problem:** This only works on your computer!

#### After:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

**What this means:**
- `import.meta.env.VITE_API_URL` - Get URL from environment variable
- `||` - "or" (if not found)
- `'http://localhost:8000/api'` - Fall back to localhost

**ELI5:** "Use the deployed backend URL in production, or localhost when developing"

**How it works:**
- **Local development:** Uses `.env.local` → `http://localhost:8000/api`
- **Production (Vercel):** Uses `.env.production` → `https://your-railway-backend.up.railway.app/api`

---

### **.env Files Explained**

#### .env.local (Development)
```
VITE_API_URL=http://localhost:8000/api
```

**When used:** `npm run dev` (local development)

#### .env.production (Production)
```
VITE_API_URL=https://your-railway-backend.up.railway.app/api
```

**When used:** `npm run build` (deployment)

**ELI5:** Like having two phone numbers - one for home, one for work

**Important Notes:**
- Vite uses `VITE_` prefix for environment variables
- Without `VITE_`, variables won't be accessible
- `.env.local` is NOT uploaded to GitHub (in .gitignore)
- `.env.production` CAN be uploaded (no secrets)

---

### **vercel.json Explained**

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

**Breaking it down:**
- `framework`: "vite" - Tells Vercel this is a Vite project
- `buildCommand`: Command to build production files
- `outputDirectory`: Where built files are located
- `installCommand`: How to install dependencies
- `devCommand`: How to run locally (for preview)

**ELI5:** "Instructions telling Vercel how to build your React app"

---

## 🚀 STEP 2: Deploy to Vercel

### **Method 1: Using Vercel CLI (Recommended)**

#### Step 1: Install Vercel CLI

```powershell
npm install -g vercel
```

**Verify installation:**
```powershell
vercel --version
```

#### Step 2: Login to Vercel

```powershell
vercel login
```

Choose login method:
- Email
- GitHub
- GitLab
- Bitbucket

**ELI5:** "Tell Vercel who you are so it knows where to deploy your app"

#### Step 3: Navigate to Frontend Directory

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react
```

#### Step 4: Update Production Environment Variable

**IMPORTANT:** Before deploying, update `.env.production` with your ACTUAL Railway backend URL!

```
VITE_API_URL=https://your-actual-railway-app.up.railway.app/api
```

**How to get your Railway URL:**
```powershell
cd ..\backend
railway domain
```

Copy the URL and add `/api` at the end.

**Example:**
```
Railway URL: https://equipment-backend-production-abc123.up.railway.app
Add /api: https://equipment-backend-production-abc123.up.railway.app/api
```

#### Step 5: Deploy!

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react
vercel
```

**What happens next:**

Vercel will ask questions:

```
? Set up and deploy "frontend-react"? Y
? Which scope do you want to deploy to? (Your name)
? Link to existing project? N
? What's your project's name? equipment-visualizer-frontend
? In which directory is your code located? ./
```

**Answers:**
1. "Set up and deploy?" → **Y** (Yes)
2. "Which scope?" → **Select your account**
3. "Link to existing project?" → **N** (No, new project)
4. "Project name?" → **equipment-visualizer-frontend**
5. "Directory?" → **./** (current directory)

Vercel will then:
- Detect Vite automatically ✅
- Install dependencies (`npm install`)
- Build your app (`npm run build`)
- Deploy to Vercel

**Wait time:** ~2-3 minutes

#### Step 6: Get Your URL

After deployment completes, you'll see:

```
✅  Production: https://equipment-visualizer-frontend.vercel.app
```

**Save this URL!** This is your deployed frontend.

---

### **Method 2: Using GitHub (Alternative)**

If you prefer connecting via GitHub:

#### Step 1: Create GitHub Repository

```powershell
cd c:\Users\91985\Desktop\FOSSE_2026\frontend-react
git init
git add .
git commit -m "Frontend ready for deployment"
```

Create repo on GitHub, then:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/equipment-frontend.git
git push -u origin main
```

#### Step 2: Connect Vercel to GitHub

1. Go to https://vercel.com
2. Click "Add New Project"
3. Click "Import Git Repository"
4. Select your frontend repository
5. Vercel auto-detects Vite!

#### Step 3: Configure Environment Variable

**CRITICAL STEP:**

Before deploying, add environment variable in Vercel dashboard:

1. In project settings
2. Go to "Environment Variables"
3. Add:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-railway-backend.up.railway.app/api`
   - **Environment:** Production

#### Step 4: Deploy

Click "Deploy" button!

Vercel deploys automatically.

---

## 🧪 STEP 3: Test Deployment

### Test 1: Check if Frontend Loads

Open your Vercel URL in browser:
```
https://equipment-visualizer-frontend.vercel.app
```

You should see your login page!

### Test 2: Check API Connection

**Open Browser Console** (F12 → Console)

Look for network requests. Should see:
```
POST https://your-railway-backend.up.railway.app/api/login/
```

**NOT:**
```
POST http://localhost:8000/api/login/ ❌
```

### Test 3: Test Login

1. Open your deployed frontend
2. Enter credentials: admin / admin123
3. Click Login

**Expected:** Successfully login, see dashboard

**If error:** Check browser console for API errors

### Test 4: Test CSV Upload

1. Login to deployed frontend
2. Go to Upload tab
3. Select `sample_equipment_data.csv`
4. Upload

**Expected:** Success message, dataset created

### Test 5: Test Charts

1. Go to Dashboard tab
2. Select uploaded dataset
3. **Expected:** Charts render, statistics show

---

## ⚠️ COMMON DEPLOYMENT MISTAKES TO AVOID

### Mistake 1: Wrong Backend URL

**Error:** "Network Error" or "Cannot connect to server"

**Fix:** Check `.env.production` has correct Railway URL

**Debug:**
```powershell
# Check what URL is being used
vercel env ls
```

### Mistake 2: Forgot `/api` at End of URL

**Wrong:**
```
VITE_API_URL=https://your-backend.railway.app
```

**Correct:**
```
VITE_API_URL=https://your-backend.railway.app/api
```

### Mistake 3: Used `REACT_APP_` Instead of `VITE_`

**Wrong:**
```
REACT_APP_API_URL=...  ❌ (This is for Create React App)
```

**Correct:**
```
VITE_API_URL=...  ✅ (This is for Vite)
```

### Mistake 4: CORS Errors

**Error:** "Access to fetch at '...' from origin '...' has been blocked by CORS policy"

**Fix:** Your Django backend already has `CORS_ALLOW_ALL_ORIGINS = True`

If you get CORS errors:
1. Check Railway backend logs
2. Ensure `corsheaders` is in `INSTALLED_APPS`
3. Ensure `CorsMiddleware` is in `MIDDLEWARE`

### Mistake 5: Environment Variable Not Loading

**Problem:** App still tries to connect to localhost

**Debug:**
1. Check Vercel dashboard → Environment Variables
2. Ensure `VITE_API_URL` is set
3. Redeploy: `vercel --prod`

**Alternative fix:**
```powershell
vercel env add VITE_API_URL production
```
Enter your Railway URL when prompted.

### Mistake 6: Cached Build

**Problem:** Changes not showing up

**Fix:** Force rebuild
```powershell
vercel --prod --force
```

---

## 🔧 STEP 4: Configure Custom Domain (Optional)

Want a custom domain like `equipment.yourdomain.com`?

### In Vercel Dashboard:

1. Go to project settings
2. Click "Domains"
3. Enter your domain
4. Follow DNS configuration instructions

### Free Domain Options:

- **Vercel default:** `your-app.vercel.app` (free, automatic)
- **Custom subdomain:** `equipment.yourdomain.com` (if you own domain)

**For academic submission:** Vercel default domain is perfectly acceptable!

---

## 📊 STEP 5: Monitor Your Deployment

### View Deployment Logs

```powershell
vercel logs
```

**ELI5:** See what happened during deployment

### Check Build Logs

In Vercel dashboard:
- Go to "Deployments"
- Click on latest deployment
- View "Build Logs"

### Analytics (Free!)

Vercel provides free analytics:
- Page views
- Performance metrics
- User engagement

Enable in: Project Settings → Analytics

---

## 🎓 ACADEMIC SUBMISSION NOTES

### What to Tell Your Evaluator:

**About Environment Variables:**
"The frontend dynamically configures API endpoints using environment variables, allowing seamless switching between development (localhost) and production (Railway backend) environments without code changes."

**About Deployment Process:**
"The React application is deployed to Vercel's CDN for optimal performance and global availability. The build process uses Vite for fast bundling and optimization, resulting in a lightweight production bundle."

**About HTTPS:**
"Both frontend (Vercel) and backend (Railway) are served over HTTPS, ensuring secure data transmission. Token-based authentication protects API endpoints."

**About Performance:**
"The frontend is statically generated and served from Vercel's global CDN, providing fast load times regardless of user location. API calls to the Railway backend are optimized with Axios interceptors for automatic token injection."

---

## 🧪 COMPLETE TESTING CHECKLIST

Before moving to Phase 3, verify:

- [ ] Frontend deployed to Vercel
- [ ] Vercel URL accessible
- [ ] Login page loads correctly
- [ ] Login functionality works (uses Railway backend)
- [ ] Dashboard loads after login
- [ ] CSV upload works
- [ ] Charts render correctly
- [ ] PDF download works
- [ ] History tab shows uploaded datasets
- [ ] Logout works
- [ ] No console errors
- [ ] Mobile responsive (test on phone)

---

## 🐛 TROUBLESHOOTING

### Problem: "Cannot find module 'vite'"

**Fix:**
```powershell
cd frontend-react
npm install
```

### Problem: "Build failed"

**Check package.json:**
```json
{
  "scripts": {
    "build": "vite build"
  }
}
```

Ensure this line exists.

### Problem: "404 Not Found on page refresh"

**Fix:** Add to `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

This handles React Router client-side routing.

### Problem: "API calls work locally but not on Vercel"

**Debug steps:**
1. Open browser console on Vercel deployment
2. Check Network tab
3. Look for API call - what URL is it calling?
4. Compare with `.env.production` value

**Fix:** Update environment variable and redeploy.

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Backend deployed to Railway (from Phase 1)
- [ ] Railway URL copied and saved
- [ ] `.env.production` updated with Railway URL
- [ ] Frontend built successfully (`npm run build` works locally)
- [ ] Deployed to Vercel
- [ ] Environment variable set in Vercel
- [ ] Login tested on deployed frontend
- [ ] CSV upload tested
- [ ] Charts working
- [ ] PDF download working

---

## 📝 SAVE YOUR DEPLOYMENT URLs

**Backend (Railway):**
```
https://equipment-backend-production-xxx.up.railway.app
```

**Frontend (Vercel):**
```
https://equipment-visualizer-frontend.vercel.app
```

**Write these down! You'll need them for:**
- Desktop app configuration (Phase 3)
- Demo presentation
- Submission documentation

---

## 🎉 PHASE 2 COMPLETE!

Your React frontend is now:
- ✅ Deployed to Vercel
- ✅ Accessible via HTTPS
- ✅ Connected to Railway backend
- ✅ Serving optimized static files from CDN
- ✅ Ready for users worldwide

**Next:** PHASE 3 - Desktop App Packaging

---

**Ready to proceed to Phase 3?**
