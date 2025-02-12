from flask import jsonify, current_app
from flask_restx import Resource
from models import api
import json
import os
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['GET'],
    description='Get observations for specified entities from the knowledge graph'
)
class Observation(Resource):
    @api.response(200, 'Observations retrieved successfully')
    @api.response(404, 'Knowledge graph or entity not found')
    @api.response(500, 'Internal Server Error')
    def get(self, entityName):
        """Get observations for specified entities"""
        try:
            storage_path = os.path.join('./api/mcp_tools/store', 'memory.json')

            if not os.path.exists(storage_path):
                return jsonify({ 'message': 'Knowledge graph not found' }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            entity_name = entityName
            if entity_name not in graph.get('entities', {}):
                return jsonify({ 'message': f'Entity {entity_name} not found' }), 404

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
