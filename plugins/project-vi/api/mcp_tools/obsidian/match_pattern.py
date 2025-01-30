from flask import jsonify, current_app
from flask_restx import Resource
from models import api, pattern_match_model
import json
import os
import logging

logger = logging.getLogger('pattern_evolution')

@api.doc(
    methods=['POST'],
    description='Find matching patterns for given content',
    responses={
        200: 'Pattern matching completed successfully',
        500: 'Internal server error'
    }
)
class MatchPattern(Resource):
    @api.expect(pattern_match_model)
    @api.response(200, 'Pattern matching completed successfully')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Find matching patterns for content"""
        try:
            data = api.payload
            content = data['content'].lower()
            threshold = data.get('threshold', 0.8)
            context = data.get('context')

            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'patterns.json')
            with open(storage_path, 'r') as f:
                patterns = json.load(f)

            matches = []

            # Check base patterns
            for prefix, pattern in patterns.get('base_patterns', {}).items():
                if context in pattern['contexts'] or not context:
                    if any(attr.lower() in content for attr in pattern['attributes']):
                        matches.append({
                            'pattern': prefix,
                            'type': 'base',
                            'confidence': pattern['confidence']
                        })

            # Check evolved patterns
            for evo_id, pattern in patterns.get('evolved_patterns', {}).items():
                if any(attr.lower() in content for attr in pattern['attributes']):
                    matches.append({
                        'pattern': evo_id,
                        'type': 'evolved',
                        'confidence': pattern['confidence'],
                        'parent': pattern['parent']
                    })

            # Filter by threshold
            matches = [m for m in matches if m['confidence'] >= threshold]

            logger.info(f'Found {len(matches)} matching patterns')
            return jsonify({'matches': matches}), 200

        except Exception as e:
            logger.error(f'Error matching patterns: {str(e)}')
            return jsonify({'error': str(e)}), 500
