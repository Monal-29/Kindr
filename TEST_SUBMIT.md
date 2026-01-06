# Testing Help Request Submission

## Quick Test (Without File)

1. **Refresh the page** (Ctrl+F5)
2. **Click "Create Help Request"**
3. **Fill in the form** (but DON'T select a file)
4. **Click "Submit Request"**

If this works, the issue is with file uploads. If it doesn't work, check the browser console.

## Check Browser Console

1. Press **F12** to open Developer Tools
2. Go to **Console** tab
3. Look for messages starting with `[Create Request]`
4. Look for any red error messages
5. Share what you see

## Check Network Tab

1. Press **F12** → **Network** tab
2. Try to submit the form
3. Look for a request to `/api/help-requests`
4. Click on it and check:
   - **Status**: What status code? (200, 201, 400, 500, etc.)
   - **Headers**: Check Request Headers and Response Headers
   - **Preview/Response**: What does the server return?

## Common Issues:

1. **Status 401**: Not logged in - login again
2. **Status 403**: Wrong user type - make sure you're logged in as recipient
3. **Status 400**: Missing required fields (title/description)
4. **CORS error**: Backend CORS not configured (should be fixed now)
5. **Failed to fetch**: Network issue or backend not running

## Try This:

Open browser console (F12) and run:
```javascript
fetch('http://127.0.0.1:5000/api/health', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

This tests if you can reach the backend with your token.

