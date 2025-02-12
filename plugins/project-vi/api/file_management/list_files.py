from flask_restx import Resource
from flask import jsonify
import os
from models import api, list_files_model


@api.doc(
    methods=['GET'],
    description='This endpoint lists files in specified directory. Default is current directory.',
    params={'directory': 'The directory to list files from'}
)
class ListFiles(Resource):
    @api.expect(list_files_model)
    @api.response(200, 'Success')
    @api.response(404, 'Directory not found')
    @api.response(500, 'Internal Server Error')
    def get(self, directory="."):
        if not os.path.exists(directory):
            return jsonify({"error": "Directory not found."}), 404
        try:
            files = os.listdir(directory)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({"files": files}), 200
