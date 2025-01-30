from flask import jsonify, current_app
from flask_restx import Resource
from models import api, add_observations_model
from datetime import datetime
import json
import os
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['POST'],
    description='Add new observations to existing entities in the knowledge graph'
)
class AddObservations(Resource):
    @api.expect(add_observations_model)
    @api.response(201, 'Observations added successfully')
    @api.response(400, 'Invalid data or entity not found')
    @api.response(404, 'Knowledge graph not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Add new observations to existing entities"""
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

            # Process observations for each entity
            for observation in data['observations']:
                entity_name = observation['entityName']
                if entity_name not in entities:
                    missing_entities.append(entity_name)
                    continue

                entity = entities[entity_name]
                # Add new observations, avoiding duplicates
                new_observations = [
                    content for content in observation['contents']
                    if content not in entity.get('observations', [])
                ]
                
                if 'observations' not in entity:
                    entity['observations'] = []
                
                entity['observations'].extend(new_observations)
                entity['updated_at'] = datetime.now().isoformat()

                results.append({
                    'entityName': entity_name,
                    'added_observations': new_observations
                })

            if missing_entities:
                return jsonify({
                    'message': 'Some entities not found',
                    'missing_entities': missing_entities
                }), 400

            # Save updated graph
            with open(storage_path, 'w') as f:
                json.dump(graph, f, indent=2)

            logger.info(f'Added observations to {len(results)} entities')
            return jsonify({
                'message': 'Observations added successfully',
                'results': results
            }), 201

        except Exception as e:
            logger.error(f'Error adding observations: {str(e)}')
            return jsonify({'error': str(e)}), 500
