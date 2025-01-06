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
            error_msg = f"File not found at path: {file_path}"
            print(error_msg)
            return jsonify({"error": error_msg}), 404
            
        try:
            print(f"Opening file in r+ mode")
            with open(file_path, 'r+', encoding='utf-8') as file:
                content = file.read()
                print(f"Successfully read {len(content)} characters")
                return jsonify({"content": content}), 200
        except Exception as e:
            error_msg = f"Error reading file {file_path}: {str(e)}"
            print(error_msg)
            return jsonify({"error": error_msg}), 500