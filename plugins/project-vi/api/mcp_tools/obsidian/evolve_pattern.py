from flask import jsonify, current_app
from flask_restx import Resource
from models import api, pattern_evolve_model
import json
import os
import logging

logger = logging.getLogger('pattern_evolution')

@api.doc(
    methods=['POST'],
    description='Evolve an existing pattern by adding new attributes and relationships',
    responses={
        201: 'Pattern successfully evolved',
        404: 'Original pattern not found',
        500: 'Internal Server Error'
    }
)
class EvolvePattern(Resource):
    @api.expect(pattern_evolve_model)
    @api.response(201, 'Pattern successfully evolved')
    @api.response(404, 'Original pattern not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Evolve an existing pattern with new attributes and relationships"""
        try:
            data = api.payload
            original = data['original_pattern']
            
            # Load patterns
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'patterns.json')
            with open(storage_path, 'r') as f:
                patterns = json.load(f)

            if original not in patterns.get('base_patterns', {}):
                return jsonify({
                    'message': f'Original pattern {original} not found'
                }), 404

            # Create evolved pattern
            base_pattern = patterns['base_patterns'][original]
            evolved_pattern = {
                'parent': original,
                'attributes': {
                    **base_pattern['attributes'],
                    **data.get('new_attributes', {})
                },
                'relationships': base_pattern['relationships'] + data.get('new_relationships', []),
                'evolution_reason': data['evolution_reason'],
                'confidence': 0.8,
                'usage_count': 0
            }

            # Add to evolved patterns
            if 'evolved_patterns' not in patterns:
                patterns['evolved_patterns'] = {}
            evolution_id = f"{original}_evolved_{len(patterns['evolved_patterns'])}"
            patterns['evolved_patterns'][evolution_id] = evolved_pattern

            # Save updated patterns
            with open(storage_path, 'w') as f:
                json.dump(patterns, f, indent=2)

            logger.info(f'Evolved pattern {original} to {evolution_id}')
            return jsonify({
                'message': f'Successfully evolved pattern: {evolution_id}',
                'evolution_id': evolution_id
            }), 201

        except Exception as e:
            logger.error(f'Error evolving pattern: {str(e)}')
            return jsonify({'error': str(e)}), 500
