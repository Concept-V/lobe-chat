from flask import jsonify, current_app
from flask_restx import Resource
from models import api, search_nodes_model
import json
import os
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['POST'],
    description='Search for nodes in the knowledge graph based on a query'
)
class SearchNodes(Resource):
    @api.expect(search_nodes_model)
    @api.response(200, 'Search completed successfully')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Search for nodes matching the query"""
        try:
            data = api.payload
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'knowledge_graph.json')

            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            query = data['query'].lower()
            results = {
                'entities': [],
                'relations': []
            }

            # Search through entities
            for name, entity in graph.get('entities', {}).items():
                if (query in name.lower() or 
                    query in entity.get('type', '').lower() or 
                    any(query in obs.lower() for obs in entity.get('observations', []))):
                    results['entities'].append({
                        'name': name,
                        **entity
                    })

            # Search through relations
            for relation in graph.get('relations', []):
                if query in relation['relationType'].lower():
                    results['relations'].append(relation)

            logger.info(f'Found {len(results["entities"])} entities and {len(results["relations"])} relations matching query')
            return jsonify({
                'results': results,
                'total_matches': len(results['entities']) + len(results['relations'])
            }), 200

        except Exception as e:
            logger.error(f'Error searching nodes: {str(e)}')
            return jsonify({'error': str(e)}), 500
