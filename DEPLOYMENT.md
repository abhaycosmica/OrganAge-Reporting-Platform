# OrganAge™ Platform - Deployment Guide

## 🎯 Choose Your Deployment Method

### **Option 1: Render.com** ⭐ RECOMMENDED
**Best for:** Team testing, completely free, independent from company website
**Time:** 5 minutes
**Cost:** FREE (with sleep after 15 min inactivity)

👉 **See `RENDER_SIMPLE.md` for step-by-step guide**

**Quick Summary:**
1. Push code to GitHub (or upload files)
2. Sign up at Render.com
3. Connect repository
4. Click "Deploy"
5. Get your link: `https://organage-platform.onrender.com`

---

### **Option 2: Railway.app** ⚡ EASIEST
**Best for:** Non-developers, drag-and-drop deployment
**Time:** 3 minutes
**Cost:** $5 free credit, then ~$5-10/month

👉 **See `RAILWAY_SIMPLE.md` for step-by-step guide**

**Quick Summary:**
1. Sign up at Railway.app
2. Upload files directly (no GitHub needed!)
3. Railway auto-deploys
4. Get your link: `https://your-app.up.railway.app`

---

### **Option 3: Hostinger** 🏢 YOUR HOSTING
**Best for:** Using your existing Hostinger account
**Time:** 15 minutes
**Cost:** Included in your plan
**⚠️ Warning:** More complex, requires cPanel configuration

👉 **See `HOSTINGER_DEPLOYMENT.md` for complete guide**

---

## 🌟 Our Recommendation

**For quick team testing:** Use **Render.com** (Option 1)
- Completely FREE
- Totally separate from your company website
- Takes 5 minutes
- Share link instantly with team

**Later, if you love it:**
- Upgrade Render to $7/month for always-on
- Or move to Railway for more features
- Or deploy to Hostinger if you want full control

---

## 📋 What You Need

**For Render (Recommended):**
- [ ] GitHub account (free)
- [ ] 5 minutes of time
- [ ] That's it!

**For Railway:**
- [ ] Railway.app account (free trial)
- [ ] 3 minutes of time
- [ ] Optional: GitHub account

**For Hostinger:**
- [ ] Hostinger Business/Cloud plan
- [ ] cPanel access
- [ ] Terminal access
- [ ] 15-20 minutes
- [ ] Technical comfort with servers

---

## 🚀 Quick Start (Render - Recommended)

See full guide in `RENDER_SIMPLE.md`, but here's the ultra-quick version:

### Step 1: Prepare Your Code
1. Download and extract the `organage_platform.zip`
2. Initialize a git repository:
   ```bash
   cd organage_platform
   git init
   git add .
   git commit -m "Initial commit"
   ```

### Step 2: Push to GitHub
1. Create a new repository on GitHub (https://github.com/new)
2. Name it: `organage-platform`
3. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/organage-platform.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select the `organage-platform` repository
5. Configure:
   - **Name**: organage-platform
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
6. Click **"Create Web Service"**

### Step 4: Access Your Site
- Render will provide a URL like: `https://organage-platform.onrender.com`
- Share this link with your team!

---

## Alternative: Deploy to PythonAnywhere (FREE)

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free "Beginner" account

### Step 2: Upload Files
1. Click **"Files"** tab
2. Upload your organage_platform folder
3. Or use **"Upload a file"** for each file

### Step 3: Set Up Web App
1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Flask"**
4. Set Python version: 3.10
5. Point to your app.py file

### Step 4: Install Dependencies
1. Open a **"Bash console"**
2. Run:
   ```bash
   pip3 install -r requirements.txt --user
   ```
3. Reload your web app

### Step 5: Access
- Your URL: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Local Testing
```bash
cd organage_platform
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000

---

## Notes
- **Free tier limitations**: 
  - Render: App may sleep after 15 min of inactivity
  - PythonAnywhere: Limited CPU seconds per day
- **Data**: User uploads are temporary and deleted on restart
- **Security**: For production, add authentication!
