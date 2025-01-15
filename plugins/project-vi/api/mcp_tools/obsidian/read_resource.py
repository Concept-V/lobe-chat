from flask_restx import Resource
from flask import jsonify
import logging
from models import api, read_resource_model
from .base import ObsidianBase

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['POST'],
    description='Read a specific resource from the Obsidian vault'
)
class ReadResource(Resource, ObsidianBase):
    @api.expect(read_resource_model)
    @api.response(200, 'Success')
    @api.response(404, 'Resource not found')
    @api.response(500, 'Internal Server Error')
    def post(self, uri):
        try:
            logger.info(f"Reading resource: {uri}")
            file_path = self.vault_path / uri.replace("obsidian://", "")
            
            if not file_path.exists():
                return jsonify({"error": "Resource not found"}), 404
                
            content = self.read_file_content(file_path)
            if content:
                return jsonify(content), 200
            return jsonify({"error": "Could not read file content"}), 500
            
        except Exception as e:
            logger.error(f"Error reading resource: {e}")
            return jsonify({"error": str(e)}), 500
