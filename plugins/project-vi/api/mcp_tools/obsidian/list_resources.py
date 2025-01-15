from flask_restx import Resource
from flask import jsonify
import logging
from models import api, list_resource_model
from .base import ObsidianBase

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['GET'],
    description='List all resources in the Obsidian vault'
)
class ListResources(Resource, ObsidianBase):
    @api.marshal_list_with(list_resource_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self):
        try:
            resources = []
            for file in self.vault_path.rglob("*.md"):
                if not any(p.startswith('.') for p in file.parts):
                    relative_path = file.relative_to(self.vault_path)
                    content = self.read_file_content(file)
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
            
            return jsonify(resources), 200
            
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            return jsonify({"error": str(e)}), 500
