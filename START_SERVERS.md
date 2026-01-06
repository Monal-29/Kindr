# How to Start the Servers

## Quick Start Guide

### Step 1: Start the Backend Server

Open a terminal/command prompt and run:

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt
python database.py  # Initialize database (only needed first time)
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Step 2: Start the Frontend Server

Open a **NEW** terminal/command prompt and run:

```bash
cd frontend
node server.js
```

You should see:
```
Server is running at http://localhost:8000/
```

### Step 3: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:8000
- **Backend API**: http://localhost:5000/api/health (to test if backend is running)

## Troubleshooting

### "Failed to fetch" Error

If you see "Failed to fetch" or "Cannot connect to server":

1. **Check if backend is running**: 
   - Open http://localhost:5000/api/health in your browser
   - You should see: `{"status":"healthy"}`

2. **Check backend terminal**:
   - Make sure you see "Running on http://0.0.0.0:5000"
   - Check for any error messages

3. **Check ports**:
   - Backend should be on port 5000
   - Frontend should be on port 8000
   - Make sure no other applications are using these ports

4. **Check CORS**:
   - The backend should have CORS enabled (already configured)
   - Make sure you're accessing frontend from http://localhost:8000 (not file://)

### Common Issues

- **Port already in use**: Change the port in `backend/app.py` or `frontend/server.js`
- **Module not found**: Run `pip install -r requirements.txt` again
- **Database error**: Delete `backend/kindr.db` and run `python database.py` again

## Testing the Connection

1. Open browser console (F12)
2. Go to http://localhost:8000
3. Try to sign up
4. Check console for any error messages
5. Check Network tab to see if requests are being sent

