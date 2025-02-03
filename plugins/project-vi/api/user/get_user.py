from flask_restx import Resource
from flask import jsonify
from pathlib import Path
from models import api, get_user_model
import json
import hashlib
import logging

logger = logging.getLogger('user-server')

@api.doc(
    methods=['GET'],
    description='Get a specific user information.'
)
class GetUser(Resource):
    @api.expect(get_user_model)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    @api.response(401, 'Invalid credentials')
    @api.response(403, 'Account suspended')
    @api.response(404, 'User not found')
    def get(self, username, password):
        try:
            # Check if username is provided
            if not username:
                return jsonify({"error": "Username is required"}), 400

            # Construct path to user's JSON file
            user_path = Path("./user/store") / f"{username}.json"
            
            # Check if user exists
            if not user_path.exists():
                return jsonify({"error": "User not found"}), 404

            try:
                # Load user data
                with open(user_path, 'r') as f:
                    user_data = json.load(f)
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid user data format"}), 400

            # Check account state
            if user_data.get('state') == 'suspended':
                return jsonify({"error": "Account is suspended"}), 403

            # Hash the provided password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Verify password
            if hashed_password != user_data.get('password'):
                return jsonify({"error": "Invalid credentials"}), 401

            # Return user data (excluding password)
            return jsonify({
                "username": username,
                "permissions": user_data.get('permissions', 0),
                "state": user_data.get('state', 'active')
            }), 200

        except Exception as e:
            logger.error(f"Error processing user request: {e}")
            return jsonify({"error": "Internal server error"}), 500
