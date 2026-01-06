from flask import Blueprint, request, jsonify
from database import get_db
from middleware import token_required

swipes_bp = Blueprint('swipes', __name__)

@swipes_bp.route('/', methods=['POST'])
@token_required
def create_swipe(user_id, email, user_type, *args, **kwargs):
    """Record a swipe action (like or pass)"""
    if user_type != 'donor':
        return jsonify({"error": "Only donors can swipe"}), 403
    
    data = request.get_json()
    help_request_id = data.get('help_request_id')
    action = data.get('action')  # 'like' or 'pass'
    
    if not help_request_id or action not in ['like', 'pass']:
        return jsonify({"error": "Invalid request"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if already swiped
    cursor.execute('SELECT id FROM swipes WHERE user_id = ? AND help_request_id = ?', 
                   (user_id, help_request_id))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Already swiped on this request"}), 400
    
    # Record swipe
    cursor.execute('''
        INSERT INTO swipes (user_id, help_request_id, action)
        VALUES (?, ?, ?)
    ''', (user_id, help_request_id, action))
    
    # If liked, create a match
    if action == 'like':
        cursor.execute('''
            INSERT INTO matches (donor_id, help_request_id, status)
            VALUES (?, ?, 'pending')
        ''', (user_id, help_request_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Swipe recorded successfully"}), 201

@swipes_bp.route('/matches', methods=['GET'])
@token_required
def get_matches(user_id, email, user_type, *args, **kwargs):
    """Get matches for the current user"""
    conn = get_db()
    cursor = conn.cursor()
    
    if user_type == 'donor':
        # Get matches where this donor liked a request
        cursor.execute('''
            SELECT m.*, hr.title, hr.description, hr.category, hr.location, hr.qr_code_path,
                   u.name as recipient_name, u.email as recipient_email
            FROM matches m
            JOIN help_requests hr ON m.help_request_id = hr.id
            JOIN users u ON hr.user_id = u.id
            WHERE m.donor_id = ?
            ORDER BY m.created_at DESC
        ''', (user_id,))
    elif user_type == 'recipient':
        # Get matches for recipient's requests
        cursor.execute('''
            SELECT m.*, hr.title, hr.description, hr.category, hr.location,
                   u.name as donor_name, u.email as donor_email
            FROM matches m
            JOIN help_requests hr ON m.help_request_id = hr.id
            JOIN users u ON m.donor_id = u.id
            WHERE hr.user_id = ?
            ORDER BY m.created_at DESC
        ''', (user_id,))
    else:
        conn.close()
        return jsonify({"error": "Invalid user type"}), 403
    
    matches = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(match) for match in matches]), 200

