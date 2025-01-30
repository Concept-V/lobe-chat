from flask import jsonify, current_app
from flask_restx import Resource
from models import api, delete_observations_model
from datetime import datetime
import json
import os
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['POST'],
    description='Delete specific observations from entities in the knowledge graph'
)
class DeleteObservations(Resource):
    @api.expect(delete_observations_model)
    @api.response(200, 'Observations deleted successfully')
    @api.response(400, 'Invalid data or entity not found')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Delete specific observations from entities"""
        try:
            data = api.payload
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'knowledge_graph.json')

            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            entities = graph.get('entities', {})
            results = []
            missing_entities = []

            # Process deletions for each entity
            for deletion in data['deletions']:
                entity_name = deletion['entityName']
                if entity_name not in entities:
                    missing_entities.append(entity_name)
                    continue

                entity = entities[entity_name]
                original_count = len(entity.get('observations', []))
                
                # Remove specified observations
                entity['observations'] = [
                    obs for obs in entity.get('observations', [])
                    if obs not in deletion['observations']
                ]
                
                deleted_count = original_count - len(entity['observations'])
                entity['updated_at'] = datetime.now().isoformat()

                results.append({
                    'entityName': entity_name,
                    'deleted_count': deleted_count
                })

            if missing_entities:
                return jsonify({
                    'message': 'Some entities not found',
                    'missing_entities': missing_entities
                }), 400

            # Save updated graph
            with open(storage_path, 'w') as f:
                json.dump(graph, f, indent=2)

            logger.info(f'Deleted observations from {len(results)} entities')
            return jsonify({
                'message': 'Observations deleted successfully',
                'results': results
            }), 200

        except Exception as e:
            logger.error(f'Error deleting observations: {str(e)}')
            return jsonify({'error': str(e)}), 500
