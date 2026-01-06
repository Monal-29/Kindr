import sqlite3
import os
import bcrypt
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'kindr.db')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK(user_type IN ('donor', 'recipient', 'admin')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Help requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            location TEXT,
            urgency TEXT,
            document_path TEXT,
            qr_code_path TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'verified', 'rejected', 'fulfilled')),
            verified_by INTEGER,
            verified_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (verified_by) REFERENCES users(id)
        )
    ''')
    
    # Swipes table (to track user interactions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS swipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            help_request_id INTEGER NOT NULL,
            action TEXT NOT NULL CHECK(action IN ('like', 'pass')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (help_request_id) REFERENCES help_requests(id),
            UNIQUE(user_id, help_request_id)
        )
    ''')
    
    # Matches table (when donor likes a request)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER NOT NULL,
            help_request_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (donor_id) REFERENCES users(id),
            FOREIGN KEY (help_request_id) REFERENCES help_requests(id)
        )
    ''')
    
    # Create default admin user (password: admin123)
    admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, name, user_type)
        VALUES (?, ?, ?, ?)
    ''', ('admin@kindr.com', admin_password, 'Admin User', 'admin'))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()

