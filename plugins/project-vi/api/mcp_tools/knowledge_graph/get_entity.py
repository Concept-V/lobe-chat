from flask import jsonify, current_app
from flask_restx import Resource
from models import api, entity_model
import json
import os
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['GET'],
    description='Get details of specific entities from the knowledge graph'
)
class GetEntity(Resource):
    @api.expect(entity_model)
    @api.response(200, 'Entities retrieved successfully')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def get(self):
        """Get all entities from the knowledge graph"""
        try:
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'knowledge_graph.json')

            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            entities = graph.get('entities', {})
            logger.info(f'Retrieved {len(entities)} entities')
            return jsonify({
                'entities': entities
            }), 200

        except Exception as e:
            logger.error(f'Error retrieving entities: {str(e)}')
            return jsonify({'error': str(e)}), 500
