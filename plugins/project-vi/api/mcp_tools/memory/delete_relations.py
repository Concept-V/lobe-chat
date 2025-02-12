from flask import jsonify, current_app
from flask_restx import Resource
from models import api, delete_relations_model
import json
import os
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['POST'],
    description='Delete specified relations from the knowledge graph'
)
class DeleteRelations(Resource):
    @api.expect(delete_relations_model)
    @api.response(200, 'Relations deleted successfully')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def post(self, relations):
        """Delete multiple relations from the knowledge graph"""
        try:
            storage_path = os.path.join('./api/mcp_tools/store', 'memory.json')

            if not os.path.exists(storage_path):
                return jsonify({ 'message': 'Knowledge graph not found' }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            if 'relations' not in graph:
                return jsonify({ 'message': 'No relations exist in the graph' }), 404

            # Track which relations are deleted
            initial_count = len(graph['relations'])
            deleted_relations = []

            # Filter out relations that match the deletion criteria
            remaining_relations = []
            for existing in graph['relations']:
                should_delete = False
                for delete_rel in relations:
                    if (existing['from'] == delete_rel['from'] and 
                        existing['to'] == delete_rel['to'] and 
                        existing['relationType'] == delete_rel['relationType']):
                        deleted_relations.append(existing)
                        should_delete = True
                        break
                if not should_delete:
                    remaining_relations.append(existing)

            graph['relations'] = remaining_relations

            # Save updated graph
            with open(storage_path, 'w') as f:
                json.dump(graph, f, indent=2)

            logger.info(f'Deleted {len(deleted_relations)} relations')
            return jsonify({
                'message': 'Relations deleted successfully',
                'initial_count': initial_count,
                'deleted_count': len(deleted_relations),
                'deleted_relations': deleted_relations
            }), 200

        except Exception as e:
            logger.error(f'Error deleting relations: {str(e)}')
            return jsonify({'error': str(e)}), 500
