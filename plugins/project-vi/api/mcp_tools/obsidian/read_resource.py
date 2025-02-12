from flask_restx import Resource
from flask import jsonify
from models import api, read_resource_model
from .base import ObsidianBase
import logging

logger = logging.getLogger('obsidian')

@api.doc(
    methods=['POST'],
    description='Read a specific resource'
)
class ReadResource(Resource):
    @api.expect(read_resource_model)
    @api.response(200, 'Success')
    @api.response(400, 'Invalid vault path')
    @api.response(404, 'Not found')
    @api.response(500, 'Internal Server Error')
    def post(self, vault_path, uri):

        if not vault_path or not uri:
            print("Invalid resource path")
            return jsonify({"error": "Invalid resource path"}), 400
        
        ObsidianBase.set_vault_path(vault_path)
        file_path = ObsidianBase.get_vault_path() / uri.replace("obsidian://", "")
        
        if not file_path.exists():
            print(f"Resource not found at path: {file_path}")
            return jsonify({"error": "Resource not found"}), 404
        
        try:
            content = ObsidianBase.read_file_content(file_path)
            if not content:
                print("Could not read resource content")
                return jsonify({"error": "Could not read resource content"}), 500
                
            print(f"Successfully read {len(content)} characters")
            return jsonify({"content": content, "length": len(content)}), 200
        
        except Exception as e:
            logger.error(f"Error reading resource: {e}")
            return jsonify({"error": str(e)}), 500
