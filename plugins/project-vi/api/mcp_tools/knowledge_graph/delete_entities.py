from flask import jsonify, current_app
from flask_restx import Resource
from models import api, delete_entities_model
import json
import os
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['POST'],
    description='Delete entities and their associated relations from the knowledge graph'
)
class DeleteEntities(Resource):
    @api.expect(delete_entities_model)
    @api.response(200, 'Entities deleted successfully')
    @api.response(404, 'One or more entities not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Delete multiple entities and their associated relations"""
        try:
            data = api.payload
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'knowledge_graph.json')

            # Check if graph exists
            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            # Load graph
            with open(storage_path, 'r') as f:
                graph = json.load(f)

            entity_names = data['entityNames']
            deleted_entities = []
            not_found = []

            # Delete entities
            for name in entity_names:
                if name in graph.get('entities', {}):
                    del graph['entities'][name]
                    deleted_entities.append(name)
                else:
                    not_found.append(name)

            # Delete associated relations if they exist
            if 'relations' in graph:
                graph['relations'] = [
                    rel for rel in graph['relations'] 
                    if rel['from'] not in entity_names and rel['to'] not in entity_names
                ]

            # Save updated graph
            with open(storage_path, 'w') as f:
                json.dump(graph, f, indent=2)

            response = {
                'message': 'Entities deleted successfully',
                'deleted_entities': deleted_entities
            }
            if not_found:
                response['not_found'] = not_found

            status_code = 200 if deleted_entities else 404
            logger.info(f'Deleted {len(deleted_entities)} entities')
            return jsonify(response), status_code

        except Exception as e:
            logger.error(f'Error deleting entities: {str(e)}')
            return jsonify({'error': str(e)}), 500
