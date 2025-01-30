from flask import jsonify, current_app
from flask_restx import Resource
from models import api, memory_query_model
import sqlite3
import json
import logging

logger = logging.getLogger('memory')

@api.doc(
    methods=['POST'],
    description='Search through stored memories with filters'
)
class QueryMemory(Resource):
    @api.expect(memory_query_model)
    @api.response(200, 'Query executed successfully')
    @api.response(500, 'Internal server error')
    def post(self):
        """Search through stored memories"""
        try:
            data = api.payload
            db_path = current_app.config['DB_PATH']
            query = data['query']
            memory_type = data.get('memory_type', 'all')

            with sqlite3.connect(db_path) as conn:
                if memory_type == 'all':
                    cursor = conn.execute(
                        'SELECT * FROM memories WHERE content LIKE ? ORDER BY created_at DESC',
                        (f'%{query}%',)
                    )
                else:
                    cursor = conn.execute(
                        'SELECT * FROM memories WHERE content LIKE ? AND memory_type = ? ORDER BY created_at DESC',
                        (f'%{query}%', memory_type)
                    )

                results = [
                    {
                        'id': row[0],
                        'content': row[1],
                        'type': row[2],
                        'created_at': row[3],
                        'metadata': json.loads(row[4]) if row[4] else {}
                    }
                    for row in cursor.fetchall()
                ]

                logger.info(f'Found {len(results)} matching memories')
                return jsonify({'results': results}), 200

        except Exception as e:
            logger.error(f'Error querying memories: {str(e)}')
            return jsonify({'error': str(e)}), 500
