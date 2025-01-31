from flask_restx import Resource
from flask import jsonify
import os
import shutil
from models import api, move_model


@api.doc(
    methods=['POST'],
    description='This endpoint moves a file or directory. Expects a POST request',
    params={
        'source_path': 'The path of the source file or directory',
        'destination_path': 'The destination path'
    }
)
class MovePath(Resource):
    @api.expect(move_model)
    @api.response(200, 'Path moved successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Source path not found')
    @api.response(500, 'Internal Server Error')
    def post(self, source_path, destination_path):
        if not source_path or not destination_path:
            return jsonify({"error": "Invalid input."}), 400
        
        if not os.path.exists(source_path):
            return jsonify({"error": "Source path not found."}), 404
            
        try:
            shutil.move(source_path, destination_path)
            
            return jsonify({
                "message": "Path moved successfully",
                "source": source_path,
                "destination": destination_path,
                "type": "file" if os.path.isfile(destination_path) else "directory"
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
