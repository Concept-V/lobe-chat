from flask_restx import Resource
from flask import jsonify
import os
from model import api, write_file_model

@api.doc(
    methods=['POST'],
    description='This endpoint writes a new file. Expects a POST request',
    params={'file_path': 'The path of the file to write', 'content': 'The content to write into the file'}
)
class WriteFile(Resource):
    @api.expect(write_file_model)
    @api.response(200, 'File written successfully')
    @api.response(400, 'Invalid input')
    @api.response(500, 'Internal Server Error')
    def post(self, file_path, content):
        print("\nDebug Info:")
        print(f"Attempting to write to file: {file_path}")
        print(f"Current working directory: {os.getcwd()}")
        
        if not file_path or not content:
            return jsonify({"error": "Invalid input."}), 400
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write with explicit UTF-8 encoding
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Successfully wrote {len(content)} characters")
        except Exception as e:
            error_msg = f"Error writing file {file_path}: {str(e)}"
            print(error_msg)
            return jsonify({"error": error_msg}), 500

        return jsonify({"message": "File written successfully."}), 200