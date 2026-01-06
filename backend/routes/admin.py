from flask import Blueprint, request, jsonify
from database import get_db
from middleware import admin_required
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/pending-requests', methods=['GET'])
@admin_required
def get_pending_requests(user_id, email, user_type, *args, **kwargs):
    """Get all pending help requests for admin verification"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT hr.*, u.name as recipient_name, u.email as recipient_email
        FROM help_requests hr
        JOIN users u ON hr.user_id = u.id
        WHERE hr.status = 'pending'
        ORDER BY hr.created_at DESC
    ''')
    
    requests = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(req) for req in requests]), 200

@admin_bp.route('/verify-request/<int:request_id>', methods=['POST'])
@admin_required
def verify_request(user_id, email, user_type, request_id, *args, **kwargs):
    """Verify or reject a help request"""
    data = request.get_json()
    action = data.get('action')  # 'verify' or 'reject'
    
    if action not in ['verify', 'reject']:
        return jsonify({"error": "Invalid action"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Update request status
    status = 'verified' if action == 'verify' else 'rejected'
    cursor.execute('''
        UPDATE help_requests
        SET status = ?, verified_by = ?, verified_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (status, user_id, request_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Request {action}ed successfully"}), 200

@admin_bp.route('/document/<int:request_id>', methods=['GET'])
@admin_required
def get_document(user_id, email, user_type, request_id, *args, **kwargs):
    """Get document path for a help request"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT document_path FROM help_requests WHERE id = ?', (request_id,))
    request_data = cursor.fetchone()
    conn.close()
    
    if not request_data or not request_data['document_path']:
        return jsonify({"error": "Document not found"}), 404
    
    document_path = os.path.join(os.path.dirname(__file__), '..', request_data['document_path'])
    
    if not os.path.exists(document_path):
        return jsonify({"error": "Document file not found"}), 404
    
    from flask import send_file
    return send_file(document_path)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats(user_id, email, user_type, *args, **kwargs):
    """Get admin dashboard statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    
    # Total requests
    cursor.execute('SELECT COUNT(*) as count FROM help_requests')
    stats['total_requests'] = cursor.fetchone()['count']
    
    # Pending requests
    cursor.execute('SELECT COUNT(*) as count FROM help_requests WHERE status = "pending"')
    stats['pending_requests'] = cursor.fetchone()['count']
    
    # Verified requests
    cursor.execute('SELECT COUNT(*) as count FROM help_requests WHERE status = "verified"')
    stats['verified_requests'] = cursor.fetchone()['count']
    
    # Total matches
    cursor.execute('SELECT COUNT(*) as count FROM matches')
    stats['total_matches'] = cursor.fetchone()['count']
    
    # Total users
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE user_type != "admin"')
    stats['total_users'] = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify(stats), 200

