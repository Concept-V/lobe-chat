from flask_restx import Resource
from flask import jsonify
import os
import shutil
from models import api, copy_model


@api.doc(
    methods=['POST'],
    description='This endpoint copies a file or directory.',
    params={
        'source_path': 'The path of the source file or directory',
        'destination_path': 'The destination path',
        'recursive': 'Recursively copy directories'
    }
)
class CopyPath(Resource):
    @api.expect(copy_model)
    @api.response(200, 'Path copied successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Source path not found')
    @api.response(500, 'Internal Server Error')
    def post(self, source_path, destination_path, recursive=False):
        if not source_path or not destination_path:
            return jsonify({"error": "Invalid input."}), 400
        
        if not os.path.exists(source_path):
            return jsonify({"error": "Source path not found."}), 404
            
        try:
            # Convert recursive to boolean if it's a string
            if isinstance(recursive, str):
                recursive = recursive.lower() == 'true'
            
            if os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)
            else:
                if recursive:
                    shutil.copytree(source_path, destination_path)
                else:
                    return jsonify({
                        "error": "Source is a directory. Use recursive=true to copy directories."
                    }), 400
            
            return jsonify({
                "message": "Path copied successfully",
                "source": source_path,
                "destination": destination_path,
                "type": "file" if os.path.isfile(source_path) else "directory"
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
