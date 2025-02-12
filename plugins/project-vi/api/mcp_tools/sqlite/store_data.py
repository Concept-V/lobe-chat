from flask_restx import Resource
from flask import jsonify
import sqlite3
import json
import logging
import os
from models import api, store_data_model

logger = logging.getLogger('sqlite-server')

@api.doc(
    methods=['POST'],
    description='Store data in the database'
)
class StoreData(Resource):
    @api.expect(store_data_model)
    @api.response(200, 'Success')
    @api.response(404, 'Database not found')
    @api.response(500, 'Internal Server Error')
    def post(self, category, content, metadata=None):
        try:
            db_path = os.path.join('./api/mcp_tools/store', 'memory.db')

            if not os.path.exists(db_path):
                return jsonify({"error": "Database not found"}), 404
            
            if metadata is None:
                metadata = {}
                
            with sqlite3.connect(db_path) as conn:
                # Create table if it doesn't exist
                conn.execute('''
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    content TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
                
                conn.execute(
                    'INSERT INTO data (category, content, metadata) VALUES (?, ?, ?)',
                    (category, content, json.dumps(metadata))
                )
                conn.commit()
                
                return jsonify({"message": "Data stored successfully"}), 200
                
        except Exception as e:
            logger.error(f"Error storing data: {e}")
            return jsonify({"error": str(e)}), 500
