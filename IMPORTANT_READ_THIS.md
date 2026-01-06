# ⚠️ IMPORTANT: You Must Access Via HTTP, Not File://

## The Problem
Your browser console shows:
```
from origin 'null' has been blocked by CORS policy
```

**Origin 'null' means you're opening the HTML file directly from your computer (file://), not from a web server.**

## The Solution

### ✅ CORRECT WAY:
1. Make sure the frontend server is running:
   ```bash
   cd frontend
   node server.js
   ```

2. Open your browser and go to:
   **http://127.0.0.1:8000** or **http://localhost:8000**

### ❌ WRONG WAY:
- Opening the HTML file directly (double-clicking it)
- Using `file:///C:/path/to/file.html` in the address bar
- This causes CORS errors because browsers block file:// from making HTTP requests

## Quick Check

Look at your browser's address bar:
- ✅ Should show: `http://127.0.0.1:8000/login.html`
- ❌ Should NOT show: `file:///D:/kindr/frontend/login.html`

## Steps to Fix Right Now:

1. **Stop opening files directly** - Don't double-click HTML files
2. **Start the frontend server** (if not running):
   ```bash
   cd frontend
   node server.js
   ```
3. **Open in browser**: http://127.0.0.1:8000
4. **Navigate to login**: http://127.0.0.1:8000/login.html

## Why This Matters

Browsers have security restrictions that prevent files opened via `file://` from making HTTP requests to other servers. This is a security feature, not a bug.

You MUST use a web server (like the Node.js server we provided) to serve the files via HTTP.

