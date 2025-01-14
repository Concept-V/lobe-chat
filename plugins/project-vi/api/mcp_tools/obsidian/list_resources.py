from flask_restx import Resource
from flask import jsonify
from pathlib import Path
import logging
import yaml
from models import api, resource_list_model

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['GET'],
    description='List all resources in the Obsidian vault'
)
class ListResources(Resource):
    @api.marshal_list_with(resource_list_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self):
        try:
            vault_path = Path("D:/06_Project_Vi/extensions/vaults/CodeBase_Test")
            resources = []
            
            for file in vault_path.rglob("*.md"):
                if not any(p.startswith('.') for p in file.parts):
                    relative_path = file.relative_to(vault_path)
                    content = file.read_text(encoding='utf-8')
                    
                    # Parse frontmatter if exists
                    description = f"Markdown file: {relative_path}"
                    if content.startswith('---'):
                        try:
                            _, frontmatter, _ = content.split('---', 2)
                            metadata = yaml.safe_load(frontmatter)
                            tags = metadata.get("tags", [])
                            if tags:
                                description += f" (tags: {', '.join(tags)})"
                        except:
                            pass
                    
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
