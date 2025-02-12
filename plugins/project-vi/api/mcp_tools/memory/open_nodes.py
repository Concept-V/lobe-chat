from flask import jsonify, current_app
from flask_restx import Resource
from models import api, open_nodes_model
import json
import os
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['POST'],
    description='Open specific nodes in the knowledge graph by their names'
)
class OpenNodes(Resource):
    @api.expect(open_nodes_model)
    @api.response(200, 'Nodes retrieved successfully')
    @api.response(404, 'Knowledge graph or nodes not found')
    @api.response(500, 'Internal Server Error')
    def post(self, names):
        """Retrieve specific nodes and their connections"""
        try:
            storage_path = os.path.join('./api/mcp_tools/store', 'memory.json')

            if not os.path.exists(storage_path):
                return jsonify({ 'message': 'Knowledge graph not found' }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            not_found = []
            nodes = {}
            related_relations = []

            # Get requested nodes
            for name in names:
                if name in graph.get('entities', {}):
                    nodes[name] = graph['entities'][name]
                else:
                    not_found.append(name)

            # Get relations involving these nodes
            for relation in graph.get('relations', []):
                if relation['from'] in names or relation['to'] in names:
                    related_relations.append(relation)

            if not nodes:
                return jsonify({
                    'message': 'No requested nodes found',
                    'not_found': not_found
                }), 404

            response = {
                'nodes': nodes,
                'relations': related_relations
            }

            if not_found:
                response['not_found'] = not_found

            logger.info(f'Retrieved {len(nodes)} nodes and {len(related_relations)} related relations')
            return jsonify(response), 200

        except Exception as e:
            logger.error(f'Error opening nodes: {str(e)}')
            return jsonify({'error': str(e)}), 500
