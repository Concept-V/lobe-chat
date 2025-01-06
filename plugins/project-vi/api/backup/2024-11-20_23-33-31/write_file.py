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
        if not file_path or not content:
            return jsonify({"error": "Invalid input."}), 400
        try:
            with open(file_path, 'w') as file:
                file.write(content)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({"message": "File written successfully."}), 200
