# Troubleshooting Connection Issues

## If you're getting "Cannot connect to server" error:

### Step 1: Verify Both Servers Are Running

**Backend (Port 5000):**
- Open http://localhost:5000/api/health in your browser
- You should see: `{"status":"healthy"}`
- If not, start the backend:
  ```bash
  cd backend
  python app.py
  ```

**Frontend (Port 8000):**
- Open http://localhost:8000 in your browser
- You should see the landing page
- If not, start the frontend:
  ```bash
  cd frontend
  node server.js
  ```

### Step 2: Check Browser Console

1. Open Developer Tools (F12)
2. Go to **Console** tab
3. Look for any red error messages
4. Common errors:
   - **CORS error**: Backend CORS not configured properly
   - **Network error**: Backend not running
   - **401/403 error**: Authentication issue

### Step 3: Check Network Tab

1. Open Developer Tools (F12)
2. Go to **Network** tab
3. Try to create a help request
4. Look for the request to `/api/help-requests`
5. Check:
   - **Status code**: Should be 200 or 201 (not 404, 500, etc.)
   - **Request URL**: Should be `http://localhost:5000/api/help-requests`
   - **Request Headers**: Should include `Authorization: Bearer <token>`

### Step 4: Verify You're Logged In

1. Open Developer Tools (F12)
2. Go to **Application** tab (or **Storage** in Firefox)
3. Click on **Local Storage** → `http://localhost:8000`
4. Check if `token` exists
5. If not, **login again**

### Step 5: Verify User Type

- Help requests can only be created by **recipients**
- If you signed up as a **donor**, you need to:
  1. Logout
  2. Sign up again as a **recipient** (select "Seek Help")
  3. Or create a new account

### Step 6: Clear Browser Cache

1. Press **Ctrl+Shift+Delete**
2. Select "Cached images and files"
3. Click "Clear data"
4. Refresh the page (Ctrl+F5)

### Step 7: Test Direct API Call

Open browser console and run:
```javascript
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

If this fails, the backend is not accessible.

### Common Issues:

1. **"Failed to fetch"**: 
   - Backend not running
   - Firewall blocking port 5000
   - Browser blocking mixed content

2. **CORS error**: 
   - Backend CORS not configured (should be fixed now)
   - Try hard refresh (Ctrl+F5)

3. **401 Unauthorized**: 
   - Not logged in
   - Token expired
   - Solution: Login again

4. **403 Forbidden**: 
   - Wrong user type (donor trying to create request)
   - Solution: Sign up as recipient

### Still Not Working?

1. Check if both servers are actually running:
   ```bash
   # Check backend
   netstat -ano | findstr :5000
   
   # Check frontend  
   netstat -ano | findstr :8000
   ```

2. Try accessing backend directly:
   - http://localhost:5000/api/health
   - Should return JSON

3. Check backend terminal for error messages

4. Share the exact error message from browser console

