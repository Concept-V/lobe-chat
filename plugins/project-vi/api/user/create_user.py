from flask_restx import Resource
from flask import jsonify
import json
import hashlib
from pathlib import Path
import logging
from models import api, create_user_model, Permissions

logger = logging.getLogger('user-server')

@api.doc(
    methods=['POST'],
    description='Create new user'
)
class CreateUser(Resource):
    @api.expect(create_user_model)
    @api.response(201, 'User created')
    @api.response(400, 'Bad Request')
    @api.response(409, 'User already exists')
    def post(self, username, password, permissions=None, state='active'):
        try:
            if not username:
                return jsonify({"error": "Username is required"}), 400
            
            if username == 'admin':
                return jsonify({"error": "Cannot create admin user"}), 403
            
            if not password:
                return jsonify({"error": "Password is required"}), 400
            
            if permissions is None:
                permissions = 0
            else:
                permissions = int(Permissions.give_permission_by_name(permissions))

            user_path = Path("./api/user/store") / f"{username.lower()}.json"
            
            if user_path.exists():
                return jsonify({"error": "User already exists"}), 409

            user_data = {
                "username": username,
                "password": hashlib.sha256(password.encode()).hexdigest(),
                "permissions": permissions,
                "state": state
            }

            user_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(user_path, 'w') as f:
                json.dump(user_data, f, indent=4)
            
            return jsonify({
                "message": "User created successfully",
                "username": username,
                "permissions": permissions,
                "state": state
            }), 201

        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return jsonify({"error": str(e)}), 500
