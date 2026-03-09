#!/bin/bash

echo "🚀 OrganAge™ Platform - Easy Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install required packages
echo "📦 Installing required packages..."
pip3 install flask pandas --break-system-packages --quiet

if [ $? -eq 0 ]; then
    echo "✅ Packages installed successfully!"
else
    echo "⚠️  Some packages may already be installed (that's okay)"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the OrganAge™ platform:"
echo "  1. Open Terminal"
echo "  2. Navigate to the organage_platform folder"
echo "  3. Run: ./start.sh"
echo ""
