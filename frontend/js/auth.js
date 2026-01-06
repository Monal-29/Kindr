// Authentication handling
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await apiCall(API_CONFIG.ENDPOINTS.AUTH.LOGIN, 'POST', {
            email,
            password
        });
        
        // Store the token and user info
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));
        localStorage.setItem('userType', response.user.userType);
        
        // Redirect based on user type - using relative paths
        const userType = response.user.userType;
        if (userType === 'admin') {
            window.location.href = 'admin-dashboard.html';
        } else if (userType === 'donor') {
            window.location.href = 'donor-dashboard.html';
        } else {
            window.location.href = 'recipient-dashboard.html';
        }
    } catch (error) {
        console.error('Login failed:', error);
        const errorDiv = document.getElementById('error-message');
        if (errorDiv) {
            // Show the actual error message
            errorDiv.textContent = error.message || 'Login failed. Please check your credentials.';
            errorDiv.style.display = 'block';
        }
    }
}

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
    }
    return token;
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userType');
    window.location.href = 'login.html';
} 