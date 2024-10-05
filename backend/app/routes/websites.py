from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import get_websites_by_user_id, create_website, update_website, delete_website
from bson import ObjectId

bp = Blueprint('websites', __name__, url_prefix='/websites')

@bp.route('', methods=['GET'])
@jwt_required()
def get_websites():
    current_user_id = get_jwt_identity()
    websites = get_websites_by_user_id(current_user_id)
    return jsonify([{**w, '_id': str(w['_id'])} for w in websites]), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_new_website():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    website_id = create_website(
        url=data['url'],
        name=data['name'],
        check_interval=data.get('check_interval', 5),
        user_id=current_user_id
    )
    
    return jsonify({"msg": "Website created successfully", "website_id": website_id}), 201

@bp.route('/<website_id>', methods=['PUT'])
@jwt_required()
def update_existing_website(website_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    update_website(website_id, {
        "url": data.get('url'),
        "name": data.get('name'),
        "check_interval": data.get('check_interval')
    })
    
    return jsonify({"msg": "Website updated successfully"}), 200

@bp.route('/<website_id>', methods=['DELETE'])
@jwt_required()
def delete_existing_website(website_id):
    current_user_id = get_jwt_identity()
    delete_website(website_id)
    return jsonify({"msg": "Website deleted successfully"}), 200