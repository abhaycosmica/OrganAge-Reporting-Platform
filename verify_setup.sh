#!/bin/bash
# OrganAge Platform - Setup Verification Script

echo "🔍 OrganAge Platform - Checking Setup..."
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment activated: $VIRTUAL_ENV"
else
    echo "⚠ Virtual environment not activated"
    echo "  Run: source ~/virtualenv/organage/3.11/bin/activate"
fi

# Check required packages
echo ""
echo "✓ Checking installed packages..."
pip list | grep -E "Flask|pandas|Werkzeug|gunicorn"

# Check folder structure
echo ""
echo "✓ Checking folder structure..."
if [ -f "app.py" ]; then echo "  ✓ app.py found"; else echo "  ✗ app.py missing"; fi
if [ -f "passenger_wsgi.py" ]; then echo "  ✓ passenger_wsgi.py found"; else echo "  ✗ passenger_wsgi.py missing"; fi
if [ -f ".htaccess" ]; then echo "  ✓ .htaccess found"; else echo "  ✗ .htaccess missing"; fi
if [ -d "templates" ]; then echo "  ✓ templates/ found"; else echo "  ✗ templates/ missing"; fi
if [ -d "static" ]; then echo "  ✓ static/ found"; else echo "  ✗ static/ missing"; fi
if [ -d "uploads" ]; then echo "  ✓ uploads/ found"; else echo "  ⚠ uploads/ missing (run: mkdir uploads)"; fi

# Check .htaccess configuration
echo ""
echo "✓ Checking .htaccess..."
if grep -q "YOUR_USERNAME" .htaccess; then
    echo "  ⚠ .htaccess still has placeholder 'YOUR_USERNAME'"
    echo "  → Update with your actual username!"
else
    echo "  ✓ .htaccess configured"
fi

echo ""
echo "📋 Setup Check Complete!"
echo ""
echo "Next steps:"
echo "1. If packages missing: pip install -r requirements.txt"
echo "2. If uploads/ missing: mkdir uploads && chmod 755 uploads"
echo "3. Update .htaccess with your username if needed"
echo "4. Restart your Python app in cPanel"
echo ""
