from flask_restx import Resource
from flask import jsonify
import os
from model import api, read_file_model

@api.doc(
    methods=['GET'],
    description='This endpoint reads an existing file content. Expects a GET request',
    params={'file_path': 'The path of the file to read'}
)
class ReadFile(Resource):
    @api.expect(read_file_model)
    @api.response(200, 'Success')
    @api.response(404, 'File not found')
    @api.response(500, 'Internal Server Error')
    def get(self, file_path):
        print("\nDebug Info:")
        print(f"Attempting to read file: {file_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"File exists: {os.path.exists(file_path)}")
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "File not found."}), 404
            
        try:
            print(f"Opening file in r+ mode")
            with open(file_path, 'r+') as file:
                content = file.read()
                print(f"Successfully read {len(content)} characters")
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return jsonify({"error": str(e)}), 500

        return jsonify({"content": content}), 200