from flask import Blueprint, request, jsonify, send_file
from database import get_db
from middleware import token_required
import os
import uuid
from werkzeug.utils import secure_filename

help_requests_bp = Blueprint('help_requests', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@help_requests_bp.route('/', methods=['POST'])
@token_required
def create_help_request(user_id, email, user_type, *args, **kwargs):
    """Create a new help request"""
    if user_type != 'recipient':
        return jsonify({"error": "Only recipients can create help requests"}), 403
    
    # Check if request is JSON or form-data
    if request.is_json:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        category = data.get('category', 'general')
        location = data.get('location', '')
        urgency = data.get('urgency', 'medium')
        document_path = None
    else:
        # Handle form-data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category', 'general')
        location = request.form.get('location', '')
        urgency = request.form.get('urgency', 'medium')
        
        # Handle file upload if present
        document_path = None
        qr_code_path = None
        
        # Helper for saving files
        def save_upload(file_obj, prefix=''):
             filename = secure_filename(file_obj.filename)
             unique_filename = f"{prefix}{uuid.uuid4()}_{filename}"
             save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
             file_obj.save(save_path)
             return f"uploads/{unique_filename}"

        if 'document' in request.files:
            file = request.files['document']
            if file and file.filename and allowed_file(file.filename):
                document_path = save_upload(file)

        if 'qr_code' in request.files:
            file = request.files['qr_code']
            if file and file.filename and allowed_image(file.filename):
                qr_code_path = save_upload(file, prefix='qr_')
    
    if not title or not description:
        return jsonify({"error": "Title and description required"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO help_requests (user_id, title, description, category, location, urgency, document_path, qr_code_path, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    ''', (user_id, title, description, category, location, urgency, document_path, qr_code_path))
    
    request_id = cursor.lastrowid
    conn.commit()
    
    # Get the created request
    cursor.execute('SELECT * FROM help_requests WHERE id = ?', (request_id,))
    help_request = cursor.fetchone()
    conn.close()
    
    return jsonify({
        "id": help_request['id'],
        "title": help_request['title'],
        "description": help_request['description'],
        "category": help_request['category'],
        "status": help_request['status'],
        "created_at": help_request['created_at']
    }), 201

@help_requests_bp.route('/verified', methods=['GET'])
@token_required
def get_verified_requests(user_id, email, user_type, *args, **kwargs):
    """Get all verified help requests (for swiping)"""
    # Only donors should be able to see verified requests for swiping
    if user_type != 'donor':
        return jsonify({"error": "Only donors can view verified requests"}), 403
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get verified requests that user hasn't swiped on
    # Exclude requests created by the donor themselves (shouldn't happen, but safety check)
    # Using LEFT JOIN is more reliable than NOT IN
    cursor.execute('''
        SELECT hr.*, u.name as recipient_name, u.email as recipient_email
        FROM help_requests hr
        JOIN users u ON hr.user_id = u.id
        LEFT JOIN swipes s ON hr.id = s.help_request_id AND s.user_id = ?
        WHERE hr.status = 'verified'
        AND hr.user_id != ?
        AND s.id IS NULL
        ORDER BY hr.created_at DESC
    ''', (user_id, user_id))
    
    requests = cursor.fetchall()
    
    # Debug: Also check total verified requests
    cursor.execute('SELECT COUNT(*) as count FROM help_requests WHERE status = ?', ('verified',))
    total_verified = cursor.fetchone()['count']
    
    # Debug: Check user's swipes
    cursor.execute('SELECT COUNT(*) as count FROM swipes WHERE user_id = ?', (user_id,))
    user_swipes = cursor.fetchone()['count']
    
    # Debug: Check if there are verified requests excluding this user's own requests
    cursor.execute('SELECT COUNT(*) as count FROM help_requests WHERE status = ? AND user_id != ?', ('verified', user_id))
    verified_excluding_own = cursor.fetchone()['count']
    
    # Debug: Get list of verified request IDs for debugging
    cursor.execute('SELECT id, user_id, title FROM help_requests WHERE status = ?', ('verified',))
    all_verified = cursor.fetchall()
    
    conn.close()
    
    # Log debug info
    print(f"[DEBUG] User {user_id} ({user_type}) requesting verified requests")
    print(f"[DEBUG] Total verified: {total_verified}, Excluding own: {verified_excluding_own}, User swipes: {user_swipes}, Available: {len(requests)}")
    print(f"[DEBUG] All verified request IDs: {[r['id'] for r in all_verified]}")
    
    result = [{
        "id": req['id'],
        "title": req['title'],
        "description": req['description'],
        "category": req['category'],
        "location": req['location'],
        "urgency": req['urgency'],
        "recipient_name": req['recipient_name'],
        "created_at": req['created_at']
    } for req in requests]
    
    # Add debug info in response headers (for development)
    response = jsonify(result)
    response.headers['X-Debug-Total-Verified'] = str(total_verified)
    response.headers['X-Debug-Verified-Excluding-Own'] = str(verified_excluding_own)
    response.headers['X-Debug-User-Swipes'] = str(user_swipes)
    response.headers['X-Debug-Available'] = str(len(result))
    response.headers['X-Debug-User-ID'] = str(user_id)
    
    return response, 200

@help_requests_bp.route('/my-requests', methods=['GET'])
@token_required
def get_my_requests(user_id, email, user_type, *args, **kwargs):
    """Get current user's help requests"""
    if user_type != 'recipient':
        return jsonify({"error": "Only recipients can view their requests"}), 403
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM help_requests WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,))
    
    requests = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(req) for req in requests]), 200

@help_requests_bp.route('/<int:request_id>', methods=['GET'])
@token_required
def get_help_request(user_id, email, user_type, request_id, *args, **kwargs):
    """Get a specific help request"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT hr.*, u.name as recipient_name, u.email as recipient_email
        FROM help_requests hr
        JOIN users u ON hr.user_id = u.id
        WHERE hr.id = ?
    ''', (request_id,))
    
    request_data = cursor.fetchone()
    conn.close()
    
    if not request_data:
        return jsonify({"error": "Help request not found"}), 404
    
    return jsonify(dict(request_data)), 200

@help_requests_bp.route('/image/<path:filename>')
def get_image(filename):
    """Serve uploaded images (QR codes, etc.)"""
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

