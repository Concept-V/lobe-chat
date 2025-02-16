from flask import jsonify, current_app
from flask_restx import Resource
from models import api
import json
import os
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['GET'],
    description='Get details of specific entities from the knowledge graph'
)
class Entity(Resource):
    @api.response(200, 'Entities retrieved successfully')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def get(self):
        """Get all entities from the knowledge graph"""
        try:
            storage_path = os.path.join('./api/mcp_tools/store', 'memory.json')

            if not os.path.exists(storage_path):
                return jsonify({ 'message': 'Knowledge graph not found' }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            entities = graph.get('entities', {})
            logger.info(f'Retrieved {len(entities)} entities')
            return jsonify({ 'entities': entities }), 200

        except Exception as e:
            logger.error(f'Error retrieving entities: {str(e)}')
            return jsonify({'error': str(e)}), 500
