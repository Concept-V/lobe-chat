from flask_restx import Resource
from flask import jsonify
import sqlite3
import logging
import os
from pathlib import Path
from models import api, execute_query_model

logger = logging.getLogger('sqlite-server')

@api.doc(
    methods=['POST'],
    description='Execute a SQL query on the database'
)
class ExecuteQuery(Resource):
    @api.expect(execute_query_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self, query):
        try:
            db_path = Path(os.getenv('APPDATA')) / 'Claude' / 'memory.db'
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.execute(query)
                
                if query.strip().lower().startswith("select"):
                    results = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    return jsonify({
                        "results": [dict(zip(columns, row)) for row in results]
                    }), 200
                else:
                    conn.commit()
                    return jsonify({"message": "Query executed successfully"}), 200
                    
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return jsonify({"error": str(e)}), 500
