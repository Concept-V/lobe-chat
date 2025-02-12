from flask import jsonify, current_app
from flask_restx import Resource
from models import api, relation_model
import json
import os
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['GET'],
    description='Get the entire knowledge graph'
)
class ReadGraph(Resource):
    @api.expect(relation_model)
    @api.response(200, 'Relations retrieved successfully')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def get(self):
        """Get all relations from the knowledge graph"""
        try:
            storage_path = os.path.join('./api/mcp_tools/store', 'memory.json')

            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            logger.info(f'Retrieved entire graph')
            return jsonify({ 'data': graph }), 200

        except Exception as e:
            logger.error(f'Error retrieving relations: {str(e)}')
            return jsonify({'error': str(e)}), 500
