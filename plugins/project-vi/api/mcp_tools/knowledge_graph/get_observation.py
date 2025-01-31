from flask import jsonify, current_app
from flask_restx import Resource
from models import api, observation_model
import json
import os
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['GET'],
    description='Get observations for specified entities from the knowledge graph'
)
class GetObservation(Resource):
    @api.expect(observation_model)
    @api.response(200, 'Observations retrieved successfully')
    @api.response(404, 'Knowledge graph or entity not found')
    @api.response(500, 'Internal Server Error')
    def get(self):
        """Get observations for specified entities"""
        try:
            data = api.payload
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'knowledge_graph.json')

            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            entity_name = data['entityName']
            if entity_name not in graph.get('entities', {}):
                return jsonify({
                    'message': f'Entity {entity_name} not found'
                }), 404

            entity = graph['entities'][entity_name]
            observations = entity.get('observations', [])

            logger.info(f'Retrieved {len(observations)} observations for entity {entity_name}')
            return jsonify({
                'entityName': entity_name,
                'observations': observations,
                'total_count': len(observations),
                'last_updated': entity.get('updated_at')
            }), 200

        except Exception as e:
            logger.error(f'Error retrieving observations: {str(e)}')
            return jsonify({'error': str(e)}), 500
