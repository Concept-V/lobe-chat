from flask_restx import Resource
from flask import jsonify
import os
from models import api, create_directory_model

@api.doc(
    methods=['POST'],
    description='This endpoint creates a new directory.',
    params={
        'directory_path': 'The path of the directory to create',
        'exist_ok': 'Do not raise an error if the directory already exists'
    }
)
class CreateDirectory(Resource):
    @api.expect(create_directory_model)
    @api.response(200, 'Directory created successfully')
    @api.response(400, 'Invalid input')
    @api.response(500, 'Internal Server Error')
    def post(self, directory_path, exist_ok=False):
        if not directory_path:
            return jsonify({"error": "Invalid input."}), 400
        
        try:
            # Convert exist_ok to boolean if it's a string
            if isinstance(exist_ok, str):
                exist_ok = exist_ok.lower() == 'true'
            
            os.makedirs(directory_path, exist_ok=exist_ok)
            return jsonify({
                "message": "Directory created successfully",
                "path": os.path.abspath(directory_path)
            }), 200
            
        except FileExistsError:
            return jsonify({
                "error": f"Directory already exists: {directory_path}"
            }), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
