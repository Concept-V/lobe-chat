from flask_restx import Resource
from flask import jsonify
from pathlib import Path
from models import api, delete_user_model
import logging
import hashlib
import json

logger = logging.getLogger('user-server')

@api.doc(
    methods=['DELETE'],
    description='Delete user'
)
class DeleteUser(Resource):
    @api.expect(delete_user_model)
    @api.response(200, 'User deleted')
    @api.response(404, 'User not found')
    def delete(self, username, password):
        try:
            if not username:
                return jsonify({"error": "Username is required"}), 400
            
            if username == 'admin':
                return jsonify({"error": "Cannot delete admin user"}), 403
            
            if not password:
                return jsonify({"error": "Password is required"}), 400

            user_path = Path("./api/user/store") / f"{username.lower()}.json"
            
            if not user_path.exists():
                return jsonify({"error": "User not found"}), 404
            
            try:
                # Load user data
                with open(user_path, 'r') as f:
                    user_data = json.load(f)

            except json.JSONDecodeError:
                return jsonify({"error": "Invalid user data format"}), 400
            
            
            # Hash the provided password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Verify password
            if hashed_password != user_data.get('password'):
                return jsonify({"error": "Invalid credentials"}), 401
            
            user_path.unlink()
            
            return jsonify({
                "message": "User deleted successfully",
                "username": username
            }), 200

        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return jsonify({"error": str(e)}), 500
