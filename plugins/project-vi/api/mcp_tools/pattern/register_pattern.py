from flask_restx import Resource
from flask import jsonify, current_app
import json
import os
from models import api, pattern_register_model
import logging

logger = logging.getLogger('pattern_evolution')

@api.doc(
    methods=['POST'],
    description='Register a new knowledge pattern in the system'
)
class RegisterPattern(Resource):
    @api.expect(pattern_register_model)
    @api.response(201, 'Pattern successfully registered')
    @api.response(400, 'Pattern already exists')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Register a new pattern in the system"""
        try:
            data = api.payload
            prefix = data['prefix']
            
            # Load existing patterns
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'patterns.json')
            patterns = {}
            if os.path.exists(storage_path):
                with open(storage_path, 'r') as f:
                    patterns = json.load(f)
            
            if prefix in patterns.get('base_patterns', {}):
                return {'message': f'Pattern with prefix {prefix} already exists'}, 400

            # Create new pattern
            pattern = {
                'prefix': prefix,
                'attributes': data.get('attributes', {}),
                'relationships': data.get('relationships', []),
                'contexts': data.get('contexts', []),
                'usage_count': 0,
                'confidence': 1.0
            }

            # Update patterns
            if 'base_patterns' not in patterns:
                patterns['base_patterns'] = {}
            patterns['base_patterns'][prefix] = pattern

            # Save to file
            os.makedirs(os.path.dirname(storage_path), exist_ok=True)
            with open(storage_path, 'w') as f:
                json.dump(patterns, f, indent=2)

            logger.info(f'Registered new pattern: {prefix}')
            return {'message': f'Successfully registered pattern: {prefix}'}, 201

        except Exception as e:
            logger.error(f'Error registering pattern: {str(e)}')
            return {'error': str(e)}, 500
