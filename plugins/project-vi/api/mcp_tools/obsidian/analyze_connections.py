from flask_restx import Resource
from flask import jsonify
import re
from pathlib import Path
import logging
from models import api, analyze_connections_model

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['POST'],
    description='Analyze connections between notes in the Obsidian vault'
)
class AnalyzeConnections(Resource):
    @api.expect(analyze_connections_model)
    @api.response(200, 'Success')
    @api.response(404, 'Note not found')
    @api.response(500, 'Internal Server Error')
    def post(self, note_path, include_backlinks=False):
        try:
            vault_path = Path("D:/06_Project_Vi/extensions/vaults/CodeBase_Test")
            full_path = vault_path / note_path
            
            if not full_path.exists():
                return jsonify({"error": f"Note not found: {note_path}"}), 404
                
            content = full_path.read_text(encoding='utf-8')
            
            # Find links and tags
            links = re.findall(r'\[\[(.*?)\]\]', content)
            tags = re.findall(r'#([\w-]+)', content)
            
            results = {
                "links": links,
                "tags": tags
            }
            
            # Add backlinks if requested
            if include_backlinks:
                backlinks = []
                note_name = full_path.stem
                for file in vault_path.rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        file_content = file.read_text(encoding='utf-8')
                        file_links = re.findall(r'\[\[(.*?)\]\]', file_content)
                        if note_name in file_links:
                            backlinks.append(str(file.relative_to(vault_path)))
                results["backlinks"] = backlinks
            
            return jsonify(results), 200
            
        except Exception as e:
            logger.error(f"Error analyzing connections: {e}")
            return jsonify({"error": str(e)}), 500
