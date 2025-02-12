from flask_restx import Resource
from flask import jsonify
from models import api, list_resources_model
from .base import ObsidianBase
import logging

logger = logging.getLogger('obsidian')

@api.doc(
    methods=['GET'],
    description='List all resources in the vault'
)
class ListResources(Resource):
    @api.expect(list_resources_model)
    @api.response(200, 'Success')
    @api.response(400, 'Invalid vault path')
    @api.response(500, 'Internal Server Error')
    def get(self, vault_path):
        if not vault_path:
            print("Invalid vault path")
            return jsonify({"error": "Invalid vault path"}), 400
        
        ObsidianBase.set_vault_path(vault_path)

        try:
            resources = []
            
            for file in ObsidianBase.get_vault_path().rglob("*.md"):
                if not any(p.startswith('.') for p in file.parts):
                    relative_path = file.relative_to(ObsidianBase.get_vault_path())
                    content = ObsidianBase.read_file_content(file)
                    description = f"Markdown file: {relative_path}"
                    
                    if content and "metadata" in content:
                        tags = content["metadata"].get("tags", [])
                        if tags:
                            description += f" (tags: {', '.join(tags)})"
                    
                    resources.append({
                        "uri": f"obsidian://{relative_path}",
                        "name": file.stem,
                        "mimeType": "text/markdown",
                        "description": description
                    })
                    
            return jsonify({"resources": resources}), 200

        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            return jsonify({"error": str(e)}), 500
