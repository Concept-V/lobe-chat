from flask_restx import Resource
from flask import jsonify
import json
from pathlib import Path
import logging
from models import api, update_user_model

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
    def put(self, username, permissions=None, state=None):
        try:
            if not username:
                return jsonify({"error": "Username is required"}), 400
            
            if username == 'admin':
                return jsonify({"error": "Cannot update admin user"}), 403

            user_path = Path("./store") / f"{username}.json"
            
            if not user_path.exists():
                return jsonify({"error": "User not found"}), 404

            with open(user_path, 'r') as f:
                user_data = json.load(f)

            if permissions is not None:
                user_data['permissions'] = permissions
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
