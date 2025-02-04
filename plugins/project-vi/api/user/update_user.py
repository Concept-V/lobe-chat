from flask_restx import Resource
from flask import jsonify
from pathlib import Path
from models import api, update_user_model, Permissions
import hashlib
import json
import logging

logger = logging.getLogger('user-server')

@api.doc(
    methods=['PUT'],
    description='Update user details'
)
class UpdateUser(Resource):
    @api.expect(update_user_model)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Bad Request')
    def put(self, username, password, permissions=None, state=None):
        try:
            if not username:
                return jsonify({"error": "Username is required"}), 400
            
            # Hash the provided password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Verify password
            if not password or hashed_password != user_data.get('password'):
                return jsonify({"error": "Invalid credentials"}), 401
            
            if username == 'admin':
                return jsonify({"error": "Cannot update admin user"}), 403

            user_path = Path("./user/store") / f"{username.lower()}.json"
            
            if not user_path.exists():
                return jsonify({"error": "User not found"}), 404

            with open(user_path, 'r') as f:
                user_data = json.load(f)

            if permissions is not None:
                user_data['permissions'] = Permissions.give_permission_by_name(permissions)

            if state is not None:
                user_data['state'] = state

            with open(user_path, 'w') as f:
                json.dump(user_data, f, indent=4)

            return jsonify({
                "message": "User updated successfully",
                "username": username,
                "permissions": user_data['permissions'],
                "state": user_data['state']
            }), 200

        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return jsonify({"error": str(e)}), 500
