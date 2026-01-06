import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'kindr.db')

def migrate():
    print(f"Connecting to database at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(help_requests)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'qr_code_path' not in columns:
            print("Adding qr_code_path column...")
            cursor.execute("ALTER TABLE help_requests ADD COLUMN qr_code_path TEXT")
            conn.commit()
            print("Migration successful: qr_code_path added.")
        else:
            print("Column qr_code_path already exists.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
