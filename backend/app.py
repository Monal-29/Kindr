from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from database import init_db

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes - more permissive settings
# Allow all origins including null (for file:// protocol)
# Note: Browsers may still block file:// origin requests for security
# Best practice: Use the frontend server (http://localhost:8000) instead of file://
CORS(app, 
     origins="*",  # Allow all origins (flask-cors handles null origin)
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=False,  # Set to False to avoid preflight issues
     max_age=3600)
# Note: Don't add CORS headers in after_request when using flask-cors - it causes duplicates

# Initialize database
init_db()

# Import routes after app initialization to avoid circular imports
from routes.auth import auth_bp
from routes.help_requests import help_requests_bp
from routes.swipes import swipes_bp
from routes.admin import admin_bp
from routes.donors import donors_bp
from routes.recipients import recipients_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(help_requests_bp, url_prefix='/api/help-requests')
app.register_blueprint(swipes_bp, url_prefix='/api/swipes')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(donors_bp, url_prefix='/api/donors')
app.register_blueprint(recipients_bp, url_prefix='/api/recipients')

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

# Handle OPTIONS preflight requests explicitly for file uploads
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        origin = request.headers.get('Origin', '*')
        response = jsonify({})
        # Allow null origin for file:// protocol
        if origin == 'null' or origin == '*':
            response.headers.add("Access-Control-Allow-Origin", "*")
        else:
            response.headers.add("Access-Control-Allow-Origin", origin)
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,X-Requested-With")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS,PATCH")
        return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 