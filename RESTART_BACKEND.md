# How to Restart the Backend Server

The backend server needs to be restarted for the CORS changes to take effect.

## Steps to Restart:

1. **Find and stop the current backend process:**
   - Open Task Manager (Ctrl+Shift+Esc)
   - Look for "python.exe" or "python" process
   - End the process, OR
   - Find the terminal window where backend is running and press Ctrl+C

2. **Restart the backend:**
   ```bash
   cd backend
   python app.py
   ```

   OR use the batch file:
   ```bash
   start-backend.bat
   ```

3. **Verify it's running:**
   - Open http://localhost:5000/api/health in your browser
   - You should see: `{"status":"healthy"}`

4. **Then try creating a help request again**

## Quick Check:

If you're still getting connection errors:
1. Make sure backend is running (check http://localhost:5000/api/health)
2. Make sure you're logged in (check browser console for token)
3. Open browser console (F12) and check for any CORS errors
4. Make sure frontend is running on http://localhost:8000 (not file://)

