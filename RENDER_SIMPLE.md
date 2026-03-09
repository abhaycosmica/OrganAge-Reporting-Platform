# OrganAge™ Platform - Simple Render Deployment (5 Minutes!)

## 🚀 Deploy to Render.com - FREE & Easy

No messing with servers, no complex setup. Just push code and go!

---

## Step 1: Push Code to GitHub (2 minutes)

### If you DON'T have git installed:
1. Go to https://github.com/new
2. Create repository named `organage-platform`
3. Click **"uploading an existing file"**
4. Drag ALL files from `organage_platform` folder
5. Click **"Commit changes"**

### If you HAVE git installed:
```bash
cd organage_platform
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/organage-platform.git
git push -u origin main
```

---

## Step 2: Deploy on Render (3 minutes)

1. Go to **https://render.com**
2. Click **"Get Started for Free"** (or sign in with GitHub)
3. Click **"New +"** → **"Web Service"**
4. Click **"Connect account"** → Authorize GitHub
5. Find `organage-platform` repository → Click **"Connect"**

6. **Configure (auto-filled from render.yaml):**
   - Name: `organage-platform` (or choose your own)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - **Instance Type**: FREE ⚠️ Make sure this is selected!

7. Click **"Create Web Service"**

8. **Wait 2-3 minutes** while Render deploys...

---

## Step 3: Get Your Link! 🎉

Once deployed (status turns green):

**Your URL:** `https://organage-platform.onrender.com`

(Or whatever name you chose)

**Share this link with your team!**

---

## ✅ That's It!

- No domain needed
- No server management  
- No complex configuration
- Completely separate from your company website

---

## 📝 Notes

**Free Tier:**
- App "sleeps" after 15 min of inactivity
- First visit after sleep takes 10-20 seconds to wake up
- Perfect for testing with your team!

**To Keep Always Awake:**
- Upgrade to paid tier: $7/month
- Or use a free uptime monitor (UptimeRobot.com) to ping it every 5 min

**Data:**
- User uploads are temporary
- Files deleted when app restarts
- For permanent storage, upgrade or use external storage

---

## 🔧 Troubleshooting

**Build Failed?**
- Check the logs in Render dashboard
- Usually means a package installation issue
- Try: Click "Manual Deploy" → "Clear build cache & deploy"

**Can't Access?**
- Check the URL in Render dashboard (under your service)
- Make sure deployment finished (green checkmark)
- Try in incognito mode (clear cache)

**Upload Not Working?**
- First visitor after sleep takes time to wake
- Give it 20 seconds and try again

---

## 🎯 Next Steps

1. Test with sample patient data
2. Share link with team
3. Gather feedback
4. If you love it and need it always-on, upgrade to $7/month

**That's it! No hosting complexity, no company website interference!**
