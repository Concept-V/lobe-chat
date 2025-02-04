from flask_restx import Resource
from flask import jsonify
from pathlib import Path
from models import api, Permissions
import json


@api.doc(
    methods=['GET'],
    description='Get user permissions'
)
class UserPermission(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    @api.response(500, 'Internal Server Error')
    def get(self, username):
        try:
            user_path = Path("./user/store") / f"{username}.json"
            
            if not user_path.exists():
                return jsonify({"error": "User not found"}), 404

            with open(user_path, 'r') as f:
                user_data = json.load(f)
                
            permissions = user_data.get('permissions', 0)
            
            return jsonify({
                "username": username,
                "permissions": permissions,
                "permissions_list": Permissions.get_permission_names(permissions)
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
