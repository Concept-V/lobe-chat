from flask_restx import Resource
from flask import jsonify
import sqlite3
import logging
import os
from models import api

logger = logging.getLogger('sqlite-server')

@api.doc(
    methods=['GET'],
    description='List all tables in the database'
)
class ListTables(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Database not found')
    @api.response(500, 'Internal Server Error')
    def get(self):
        try:
            db_path = os.path.join('./api/mcp_tools/store', 'memory.db')

            if not os.path.exists(db_path):
                return jsonify({"error": "Database not found"}), 404
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                return jsonify({"tables": tables}), 200
                
        except Exception as e:
            logger.error(f"Error listing tables: {e}")
            return jsonify({"error": str(e)}), 500
