from flask import Blueprint, request, jsonify

listings_bp = Blueprint('listings', __name__)

# Mock data - replace with database in production
listings = []

@listings_bp.route('/', methods=['GET'])
def get_listings():
    return jsonify(listings), 200

@listings_bp.route('/', methods=['POST'])
def create_listing():
    data = request.get_json()
    new_listing = {
        'id': len(listings) + 1,
        'title': data.get('title'),
        'description': data.get('description'),
        'donor_id': data.get('donor_id'),
        'status': 'available',
        'created_at': data.get('created_at')
    }
    listings.append(new_listing)
    return jsonify(new_listing), 201

@listings_bp.route('/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = next((item for item in listings if item['id'] == listing_id), None)
    if listing:
        return jsonify(listing), 200
    return jsonify({"error": "Listing not found"}), 404 