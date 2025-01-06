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
        print("The file path is: ", file_path)
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "File not found."}), 404
        try:
            # Try reading with w+ mode like edit_file.py
            with open(file_path, 'r+') as file:
                content = file.read()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({"content": content}), 200