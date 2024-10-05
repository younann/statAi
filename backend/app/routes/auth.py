# backend/app/routes/auth.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import bcrypt
from app.database import get_user_by_username, create_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if get_user_by_username(data['username']):
        return jsonify({"msg": "Username already exists"}), 400
    
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_id = create_user(data['username'], data['email'], password_hash)
    
    return jsonify({"msg": "User created successfully", "user_id": user_id}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = get_user_by_username(data['username'])
    if user and bcrypt.check_password_hash(user['password_hash'], data['password']):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid username or password"}), 401