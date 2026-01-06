# Quick Fix for Connection Issues

## If you see "Cannot connect to server":

### Step 1: Verify Backend is Running
Open this URL in your browser: **http://localhost:5000/api/health**

You should see: `{"status":"healthy"}`

If you see an error, the backend is not running. Start it:
```bash
cd backend
python app.py
```

### Step 2: Verify Frontend is Running
Open this URL: **http://localhost:8000**

You should see the landing page.

If not, start it:
```bash
cd frontend
node server.js
```

### Step 3: Clear Browser Cache
1. Press **Ctrl+Shift+Delete**
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh page with **Ctrl+F5**

### Step 4: Check Browser Console
1. Press **F12** to open Developer Tools
2. Go to **Console** tab
3. Look for any red error messages
4. Share the exact error you see

### Step 5: Make Sure You're Using HTTP (not file://)
- ✅ Correct: `http://localhost:8000`
- ❌ Wrong: `file:///C:/path/to/file.html`

### Step 6: Try Different Browser
Sometimes browsers block localhost connections. Try:
- Chrome
- Firefox
- Edge

### Step 7: Check Firewall
Windows Firewall might be blocking port 5000. Temporarily disable it to test.

### Step 8: Restart Both Servers
1. Stop backend (Ctrl+C in terminal)
2. Stop frontend (Ctrl+C in terminal)
3. Start backend: `cd backend && python app.py`
4. Start frontend: `cd frontend && node server.js`

## Still Not Working?

Open browser console (F12) and run this test:
```javascript
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

If this fails, there's a network/firewall issue blocking the connection.

