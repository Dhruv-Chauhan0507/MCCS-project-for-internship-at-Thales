# flask_app/routes/credential_routes.py

from flask import Blueprint, request, jsonify
import sys
sys.path.append('..')

from CREDENTIALS import credentials_handler

credential_bp = Blueprint('credentials', __name__)

@credential_bp.route('/create', methods=['POST'])
def create_credential():
    data = request.json
    username = data.get('username')
    credential_name = data.get('credential_name')
    credential_value = data.get('credential_value')  # plaintext or encrypted

    if not all([username, credential_name, credential_value]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        credentials_handler.create_credential(username, credential_name, credential_value)
        return jsonify({"message": "Credential stored successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@credential_bp.route('/list/<username>', methods=['GET'])
def list_credentials(username):
    try:
        credentials = credentials_handler.get_credentials_for_user(username)
        return jsonify({"username": username, "credentials": credentials})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
