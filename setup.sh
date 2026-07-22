#!/bin/bash

# Alzheimer's Disease Classification - Setup and Run Script

echo "🧠 Alzheimer's Disease Classification Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Place your 'alzheimers_disease_data.csv' in the repository root directory"
echo "2. Run the app with: streamlit run app.py"
echo ""
echo "🚀 To run the app:"
echo "   streamlit run app.py"
echo ""