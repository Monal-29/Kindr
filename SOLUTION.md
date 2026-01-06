# Solution for "Failed to fetch" Error

## The Problem
The browser is blocking the fetch request to the backend. This is usually a browser security issue.

## Solutions (Try in order):

### Solution 1: Check Browser Console
1. Press **F12** to open Developer Tools
2. Go to **Console** tab
3. Look for CORS errors or network errors
4. Share the exact error message

### Solution 2: Verify You're Using HTTP (Not file://)
- ✅ **Correct**: `http://localhost:8000`
- ❌ **Wrong**: `file:///C:/path/to/file.html`

If you see `file://` in the address bar, you need to access via the web server.

### Solution 3: Try Different Browser
Some browsers have stricter security:
- Try **Chrome**
- Try **Firefox**  
- Try **Edge**

### Solution 4: Disable Browser Extensions
Extensions like ad blockers can block localhost:
1. Open browser in **Incognito/Private mode**
2. Try accessing the site
3. If it works, an extension is blocking it

### Solution 5: Check Windows Firewall
1. Open **Windows Defender Firewall**
2. Click **Allow an app or feature**
3. Make sure **Python** is allowed
4. Or temporarily disable firewall to test

### Solution 6: Use 127.0.0.1 Instead of localhost
Sometimes `localhost` is blocked. Try changing the API URL:

In `frontend/js/config.js`, change:
```javascript
BASE_URL: 'http://127.0.0.1:5000/api',
```

### Solution 7: Check if Backend is Actually Running
Open this in your browser: **http://localhost:5000/api/health**

You should see: `{"status":"healthy"}`

If you see an error, the backend isn't running. Start it:
```bash
cd backend
python app.py
```

### Solution 8: Clear Browser Cache and Cookies
1. Press **Ctrl+Shift+Delete**
2. Select "Cached images and files" and "Cookies"
3. Click "Clear data"
4. Restart browser

### Solution 9: Check Network Tab
1. Press **F12** → **Network** tab
2. Try to login/create request
3. Look for the request to `/api/auth/login` or `/api/help-requests`
4. Click on it and check:
   - **Status**: Should be 200 or 201 (not blocked)
   - **Headers**: Check if CORS headers are present
   - **Preview/Response**: See what the server returned

## Most Common Fix:
**Make sure you're accessing via `http://localhost:8000` and not `file://`**

The backend is running correctly. The issue is browser security blocking the connection.

