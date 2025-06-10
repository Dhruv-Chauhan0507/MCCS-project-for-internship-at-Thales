# flask_app/routes/user_routes.py

from flask import Blueprint, request, jsonify
import sys
sys.path.append('..')  # Ensure your main project modules are accessible

from RBAC import rbac_handler

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'User')

    try:
        rbac_handler.register_user(username, password, role)
        return jsonify({"message": "User registered."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if rbac_handler.login_user(username, password):
        return jsonify({"message": "Login successful."})
    else:
        return jsonify({"error": "Invalid credentials."}), 401
