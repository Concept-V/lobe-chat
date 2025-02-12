from flask import jsonify
from flask_restx import Resource
from models import api, create_entities_model
from datetime import datetime
import json
import os
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['POST'],
    description='Create new entities in the knowledge graph'
)
class CreateEntities(Resource):
    @api.expect(create_entities_model)
    @api.response(201, 'Entities created successfully')
    @api.response(400, 'Invalid entity data')
    @api.response(500, 'Internal Server Error')
    def post(self, entities):
        """Create multiple new entities in the knowledge graph"""
        try:
            storage_path = os.path.join('./api/mcp_tools/store', 'memory.json')
            
            # Load existing graph
            graph = {}
            if os.path.exists(storage_path):
                with open(storage_path, 'r') as f:
                    graph = json.load(f)

            if 'entities' not in graph:
                graph['entities'] = {}

            # Process new entities
            created_entities = []
            for entity in entities:
                name = entity['name']
                
                # Check for duplicates
                if name in graph['entities']:
                    return jsonify({
                        'message': f'Entity with name {name} already exists',
                        'created_entities': created_entities
                    }), 400

                # Store new entity
                graph['entities'][name] = {
                    'type': entity['entityType'],
                    'observations': entity['observations'],
                    'created_at': datetime.now().isoformat()
                }
                created_entities.append(name)

            # Save updated graph
            os.makedirs(os.path.dirname(storage_path), exist_ok=True)
            with open(storage_path, 'w') as f:
                json.dump(graph, f, indent=2)

            logger.info(f'Created {len(created_entities)} new entities')
            return jsonify({
                'message': 'Entities created successfully',
                'created_entities': created_entities
            }), 201

        except Exception as e:
            logger.error(f'Error creating entities: {str(e)}')
            return jsonify({'error': str(e)}), 500
