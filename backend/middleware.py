from functools import wraps
from flask import request, jsonify
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
ALGORITHM = "HS256"

def token_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_user_id = data.get('user_id')
            current_user_email = data.get('email')
            current_user_type = data.get('user_type')
        except JWTError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user_id, current_user_email, current_user_type, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @token_required
    def decorated(user_id, email, user_type, *args, **kwargs):
        if user_type != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(user_id, email, user_type, *args, **kwargs)
    
    return decorated

