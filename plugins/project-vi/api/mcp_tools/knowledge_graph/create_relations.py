from flask import jsonify, current_app
from flask_restx import Resource
from models import api, create_relations_model
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger('knowledge_graph')

@api.doc(
    methods=['POST'],
    description='Create new relations between entities in the knowledge graph'
)
class CreateRelations(Resource):
    @api.expect(create_relations_model)
    @api.response(201, 'Relations created successfully')
    @api.response(400, 'Invalid relation data or entities not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Create multiple new relations between entities"""
        try:
            data = api.payload
            storage_path = os.path.join(current_app.config['STORAGE_PATH'], 'knowledge_graph.json')
            
            # Load existing graph
            if not os.path.exists(storage_path):
                return jsonify({
                    'message': 'Knowledge graph not found'
                }), 404

            with open(storage_path, 'r') as f:
                graph = json.load(f)

            if 'relations' not in graph:
                graph['relations'] = []
            
            # Validate entities exist
            entities = graph.get('entities', {})
            missing_entities = []
            created_relations = []
            
            for relation in data['relations']:
                from_entity = relation['from']
                to_entity = relation['to']
                
                # Check if entities exist
                if from_entity not in entities:
                    missing_entities.append(from_entity)
                if to_entity not in entities:
                    missing_entities.append(to_entity)
            
            if missing_entities:
                return jsonify({
                    'message': 'Some entities do not exist',
                    'missing_entities': list(set(missing_entities))
                }), 400

            # Create relations
            for relation in data['relations']:
                new_relation = {
                    'from': relation['from'],
                    'to': relation['to'],
                    'relationType': relation['relationType'],
                    'created_at': datetime.now().isoformat()
                }
                graph['relations'].append(new_relation)
                created_relations.append(new_relation)

            # Save updated graph
            with open(storage_path, 'w') as f:
                json.dump(graph, f, indent=2)

            logger.info(f'Created {len(created_relations)} new relations')
            return jsonify({
                'message': 'Relations created successfully',
                'created_relations': created_relations
            }), 201

        except Exception as e:
            logger.error(f'Error creating relations: {str(e)}')
            return jsonify({'error': str(e)}), 500
