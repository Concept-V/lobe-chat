from flask_restx import Resource
from flask import jsonify
import os
import shutil
from models import api, delete_model


@api.doc(
    methods=['POST'],
    description='This endpoint deletes a file or directory.',
    params={
        'path': 'The path of the file or directory to delete',
        'recursive': 'Recursively delete directories'
    }
)
class DeletePath(Resource):
    @api.expect(delete_model)
    @api.response(200, 'Path deleted successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Path not found')
    @api.response(500, 'Internal Server Error')
    def post(self, path, recursive=False):
        if not path:
            return jsonify({"error": "Invalid input."}), 400
        
        if not os.path.exists(path):
            return jsonify({"error": "Path not found."}), 404
            
        try:
            # Convert recursive to boolean if it's a string
            if isinstance(recursive, str):
                recursive = recursive.lower() == 'true'
            
            if os.path.isfile(path):
                os.remove(path)
            else:
                if recursive:
                    shutil.rmtree(path)
                else:
                    os.rmdir(path)
            
            return jsonify({
                "message": "Path deleted successfully",
                "path": path,
                "type": "file" if os.path.isfile(path) else "directory"
            }), 200
            
        except OSError as e:
            if not recursive and os.path.isdir(path):
                return jsonify({
                    "error": "Directory not empty. Use recursive=true to delete non-empty directories."
                }), 400
            return jsonify({"error": str(e)}), 500
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
