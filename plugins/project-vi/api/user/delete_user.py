from flask_restx import Resource
from flask import jsonify
from pathlib import Path
import logging
from models import api, delete_user_model

logger = logging.getLogger('user-server')

@api.doc(
    methods=['DELETE'],
    description='Delete user'
)
class DeleteUser(Resource):
    @api.expect(delete_user_model)
    @api.response(200, 'User deleted')
    @api.response(404, 'User not found')
    def delete(self, username):
        try:
            if not username:
                return jsonify({"error": "Username is required"}), 400
            
            if username == 'admin':
                return jsonify({"error": "Cannot delete admin user"}), 403

            user_path = Path("./store") / f"{username}.json"
            
            if not user_path.exists():
                return jsonify({"error": "User not found"}), 404

            user_path.unlink()
            
            return jsonify({
                "message": "User deleted successfully",
                "username": username
            }), 200

        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return jsonify({"error": str(e)}), 500
