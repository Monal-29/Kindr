#!/bin/bash
echo "Starting Backend Server..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "Initializing database..."
python database.py
echo ""
echo "Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py

