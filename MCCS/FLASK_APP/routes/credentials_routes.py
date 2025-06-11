from flask import Blueprint, request, jsonify
from CREDENTIALS import credentials_handler as ch
from RBAC.rbac_handler import check_permission

credential_bp = Blueprint('credentials', __name__)


# --- CREATE CREDENTIAL ---
@credential_bp.route('/credentials', methods=['POST'])
def create_credential():
    data = request.json
    username = data.get('username')
    name = data.get('name')
    password = data.get('password')
    metadata = data.get('metadata', {})

    if not check_permission(username, 'store_credential'):
        return jsonify({'error': 'Access denied'}), 403

    result = ch.store_credential(username, name, password, metadata)
    return jsonify({'message': result or 'Credential stored'}), 201


# --- GET CREDENTIAL BY ID ---
@credential_bp.route('/credentials/<int:cred_id>', methods=['GET'])
def get_credential(cred_id):
    username = request.args.get('username')

    if not check_permission(username, 'get_credential'):
        return jsonify({'error': 'Access denied'}), 403

    result = ch.get_credential(username, cred_id)
    if result:
        return jsonify(result)
    return jsonify({'error': 'Credential not found'}), 404


# --- DELETE CREDENTIAL ---
@credential_bp.route('/credentials/<int:cred_id>', methods=['DELETE'])
def delete_credential(cred_id):
    username = request.args.get('username')

    if not check_permission(username, 'delete_credential'):
        return jsonify({'error': 'Access denied'}), 403

    result = ch.delete_credential(username, cred_id)
    return jsonify({'message': result or 'Credential deleted'}), 200


# --- LIST USER'S CREDENTIALS ---
@credential_bp.route('/credentials', methods=['GET'])
def list_credentials():
    username = request.args.get('username')

    if not check_permission(username, 'list_credentials'):
        return jsonify({'error': 'Access denied'}), 403

    creds = ch.list_credentials(username)
    return jsonify({'credentials': creds})


# --- UPDATE CREDENTIAL (new route) ---
@credential_bp.route('/credentials/<int:cred_id>', methods=['PUT'])
def update_credential(cred_id):
    data = request.json
    username = data.get('username')
    new_password = data.get('password')
    new_metadata = data.get('metadata', {})

    if not check_permission(username, 'update_credential'):
        return jsonify({'error': 'Access denied'}), 403

    result = ch.update_credential(username, cred_id, new_password, new_metadata)
    if result:
        return jsonify({'message': result})
    return jsonify({'error': 'Update failed or not authorized'}), 400
