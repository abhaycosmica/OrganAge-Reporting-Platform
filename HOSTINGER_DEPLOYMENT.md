# OrganAge™ Platform - Hostinger Deployment Guide

## 🚀 Deploy to Hostinger (Step-by-Step)

### Prerequisites
- Hostinger account with Python support (Business/Cloud plans)
- cPanel access
- Domain or subdomain configured

---

## Step 1: Prepare Your Files

1. **Download and extract** `organage_platform.zip`
2. **Locate these files** - you'll upload them all

---

## Step 2: Access Hostinger cPanel

1. Log into your Hostinger account
2. Go to **Hosting** → **Manage** → **cPanel**
3. Or direct URL: `https://cpanel.hostinger.com`

---

## Step 3: Create Python Application

### Option A: Using Setup Python App (Recommended)

1. In cPanel, find **"Setup Python App"** (Software section)
2. Click **"Create Application"**
3. Configure:
   - **Python version**: 3.11 (or latest available)
   - **Application root**: `organage` (or your preferred folder name)
   - **Application URL**: Choose your domain/subdomain
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`
4. Click **"Create"**

5. **Note the paths shown** - you'll need:
   - Virtual environment path (e.g., `/home/u123456/virtualenv/organage/3.11`)
   - Application root (e.g., `/home/u123456/organage`)

---

## Step 4: Upload Your Files

### Using File Manager:

1. In cPanel, open **File Manager**
2. Navigate to your application folder (e.g., `/home/u123456/organage`)
3. Upload ALL files from `organage_platform` folder:
   - `app.py`
   - `passenger_wsgi.py`
   - `requirements.txt`
   - `.htaccess`
   - `templates/` folder
   - `static/` folder
   - All other files/folders

### OR Using FTP:

1. Use FileZilla or any FTP client
2. Connect using credentials from Hostinger
3. Upload to the application folder

---

## Step 5: Update .htaccess

1. Open `.htaccess` in File Manager
2. **Replace** `YOUR_USERNAME` with your actual username:
   - Find your username in cPanel (top right)
   - Example: if username is `u123456789`, update:
     ```
     PassengerAppRoot /home/u123456789/organage
     PassengerPython /home/u123456789/virtualenv/organage/3.11/bin/python
     ```
3. **Save** the file

---

## Step 6: Install Python Dependencies

1. In cPanel, open **"Terminal"** or **"SSH Access"**
   
2. Navigate to your virtual environment:
   ```bash
   cd ~/organage
   source ~/virtualenv/organage/3.11/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify installation:
   ```bash
   pip list
   ```
   
   You should see:
   - Flask
   - pandas
   - Werkzeug
   - gunicorn

---

## Step 7: Create Required Folders

Still in Terminal:

```bash
cd ~/organage
mkdir -p uploads
mkdir -p static/images/organs
chmod 755 uploads
```

---

## Step 8: Restart Application

1. Go back to **"Setup Python App"** in cPanel
2. Find your application
3. Click **"Restart"** button
4. Wait 10-15 seconds

---

## Step 9: Test Your Application

1. Visit your domain: `https://yourdomain.com`
   - Or subdomain: `https://organage.yourdomain.com`

2. You should see the **OrganAge intake page**

3. Try uploading test patient data

---

## Troubleshooting

### Error 500 / Application Won't Start

**Check logs:**
1. In cPanel → **Errors** → **Error Log**
2. Look for Python errors

**Common fixes:**
- Verify `.htaccess` has correct username paths
- Ensure all dependencies installed: `pip list`
- Check file permissions: uploads folder needs 755
- Restart the application

### Can't Find "Setup Python App"

- Your Hostinger plan may not support Python
- Required: Business, Cloud, or VPS plans
- Contact Hostinger support to enable Python

### Module Not Found Errors

```bash
source ~/virtualenv/organage/3.11/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Upload Folder Permissions

```bash
cd ~/organage
chmod -R 755 uploads
chown -R $USER:$USER uploads
```

---

## Production Checklist

- [ ] Python app created and started
- [ ] All files uploaded
- [ ] .htaccess updated with correct paths
- [ ] Dependencies installed
- [ ] uploads folder created with correct permissions
- [ ] Application restarted
- [ ] Domain/subdomain configured
- [ ] SSL certificate enabled (Hostinger provides free SSL)
- [ ] Test upload with sample data

---

## Security Recommendations

1. **Enable SSL** (free with Hostinger)
   - cPanel → SSL/TLS → Let's Encrypt

2. **Add password protection** (optional for testing)
   - cPanel → Directory Privacy

3. **Regular backups**
   - Hostinger has automatic backups
   - Also export data regularly

---

## Update Application

To update later:

1. Upload new files via File Manager/FTP
2. Go to "Setup Python App"
3. Click "Restart"

---

## Support

- **Hostinger Docs**: https://support.hostinger.com
- **Python Apps Guide**: Search "Python application" in Hostinger knowledge base
- **24/7 Support**: Available in your Hostinger dashboard

---

## Quick Reference

**Common Paths** (replace YOUR_USERNAME):
- App root: `/home/YOUR_USERNAME/organage`
- Virtual env: `/home/YOUR_USERNAME/virtualenv/organage/3.11`
- Python binary: `/home/YOUR_USERNAME/virtualenv/organage/3.11/bin/python`
- Public HTML: `/home/YOUR_USERNAME/public_html`

**Key Files:**
- `passenger_wsgi.py` - WSGI entry point
- `.htaccess` - Apache/Passenger configuration
- `app.py` - Flask application
- `requirements.txt` - Python dependencies
