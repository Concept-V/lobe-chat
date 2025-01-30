from flask import jsonify, current_app
from flask_restx import Resource
from models import api, memory_store_model
from datetime import datetime
import sqlite3
import json
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['POST'],
    description='Store new information in the memory database'
)
class StoreMemory(Resource):
    @api.expect(memory_store_model)
    @api.response(201, 'Memory stored successfully')
    @api.response(500, 'Internal server error')
    def post(self):
        """Store new information in memory"""
        try:
            data = api.payload
            db_path = current_app.config['DB_PATH']

            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    'INSERT INTO memories (content, memory_type, created_at, metadata) VALUES (?, ?, ?, ?)',
                    (
                        data['content'],
                        data['memory_type'],
                        datetime.now().isoformat(),
                        json.dumps(data.get('metadata', {}))
                    )
                )

            logger.info('Memory stored successfully')
            return jsonify({'message': 'Memory stored successfully'}), 201

        except Exception as e:
            logger.error(f'Error storing memory: {str(e)}')
            return jsonify({'error': str(e)}), 500
