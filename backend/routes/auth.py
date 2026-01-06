from flask import Blueprint, request, jsonify
import bcrypt
from jose import jwt
import os
from datetime import datetime, timedelta
from database import get_db

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
ALGORITHM = "HS256"

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Verify password
    if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        access_token = create_access_token(user['id'], user['email'], user['user_type'])
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user['name'],
                "userType": user['user_type']
            }
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    user_type = data.get('userType', 'recipient')  # 'donor' or 'recipient'
    
    if not email or not password or not name:
        return jsonify({"error": "Email, password, and name required"}), 400
    
    if user_type not in ['donor', 'recipient']:
        return jsonify({"error": "Invalid user type"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Email already registered"}), 400
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Insert user
    cursor.execute('''
        INSERT INTO users (email, password_hash, name, user_type)
        VALUES (?, ?, ?, ?)
    ''', (email, hashed_password, name, user_type))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user_id,
            "email": email,
            "name": name,
            "userType": user_type
        }
    }), 201

def create_access_token(user_id, email, user_type):
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode = {
        "exp": expire,
        "user_id": user_id,
        "email": email,
        "user_type": user_type
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 