# flask_app/routes/vault_routes.py

from flask import Blueprint, request, jsonify
import sys
sys.path.append('..')

from VAULT.vault import vault_handler

vault_bp = Blueprint('vault', __name__)

@vault_bp.route('/store', methods=['POST'])
def store_key():
    data = request.json
    key_id = data.get('key_id')
    key_data = data.get('key_data')  # assumed to be base64 or raw
    owner = data.get('owner')

    if not all([key_id, key_data, owner]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        vault_handler.store_key(key_id, key_data, owner)
        return jsonify({"message": f"Key '{key_id}' stored successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vault_bp.route('/get/<key_id>', methods=['GET'])
def get_key(key_id):
    try:
        key_data = vault_handler.retrieve_key(key_id)
        return jsonify({"key_id": key_id, "key_data": key_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 404
