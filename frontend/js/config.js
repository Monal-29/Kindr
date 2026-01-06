const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:5000/api',
    // Test backend connection
    async testConnection() {
        try {
            // Simple fetch without extra headers to avoid CORS preflight
            const response = await fetch('http://127.0.0.1:5000/api/health');
            return response.ok;
        } catch (error) {
            console.error('Backend connection test failed:', error);
            return false;
        }
    },
    ENDPOINTS: {
        AUTH: {
            LOGIN: '/auth/login',
            REGISTER: '/auth/register'
        },
        HELP_REQUESTS: {
            CREATE: '/help-requests',
            GET_VERIFIED: '/help-requests/verified',
            GET_MY_REQUESTS: '/help-requests/my-requests',
            GET_ONE: (id) => `/help-requests/${id}`
        },
        SWIPES: {
            CREATE: '/swipes',
            GET_MATCHES: '/swipes/matches'
        },
        ADMIN: {
            PENDING_REQUESTS: '/admin/pending-requests',
            VERIFY_REQUEST: (id) => `/admin/verify-request/${id}`,
            GET_DOCUMENT: (id) => `/admin/document/${id}`,
            STATS: '/admin/stats'
        }
    }
};

// Helper function to make API calls
async function apiCall(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        method,
        headers
        // Removed credentials: 'include' as it can cause CORS issues
    };
    
    if (data) {
        config.body = JSON.stringify(data);
    }
    
    try {
        const url = `${API_CONFIG.BASE_URL}${endpoint}`;
        console.log(`[API] ${method} ${url}`);
        
        const response = await fetch(url, config);
        
        console.log(`[API] Response status: ${response.status}`);
        
        // Check if response is ok before trying to parse JSON
        if (!response.ok) {
            let errorMessage = 'API call failed';
            try {
                const result = await response.json();
                errorMessage = result.error || errorMessage;
            } catch (e) {
                errorMessage = `Server error: ${response.status} ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('[API] Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        
        // Only show connection error for actual network failures
        if (error.name === 'TypeError' && (error.message.includes('Failed to fetch') || error.message.includes('NetworkError') || error.message.includes('Load failed'))) {
            // Don't throw immediately - try to get more info
            const errorMsg = `Network error: ${error.message}. 

Quick fixes:
1. Open http://127.0.0.1:5000/api/health in browser - should show {"status":"healthy"}
2. Try different browser (Chrome/Firefox/Edge)
3. Try incognito/private mode
4. Make sure you're using http://127.0.0.1:8000 (not file://)
5. Check browser console (F12) for details`;
            
            console.error('[API]', errorMsg);
            throw new Error(errorMsg);
        }
        // For other errors (like 401, 400, etc.), just throw the original error
        throw error;
    }
} 