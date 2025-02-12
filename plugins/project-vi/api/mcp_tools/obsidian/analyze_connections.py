from flask_restx import Resource
from flask import jsonify
from models import api, analyze_connections_model
from .base import ObsidianBase
import logging

logger = logging.getLogger('obsidian')

@api.doc(
    methods=['POST'],
    description='Analyze connections between notes'
)
class AnalyzeConnections(Resource):
    @api.expect(analyze_connections_model)
    @api.response(200, 'Success')
    @api.response(400, 'Invalid vault path')
    @api.response(404, 'Note not found')
    @api.response(500, 'Internal Server Error')
    def post(self, vault_path, note_path, include_backlinks=False):
        if not vault_path:
            return jsonify({"error": "Invalid vault path"}), 400
        
        ObsidianBase.set_vault_path(vault_path)
        full_path = ObsidianBase.get_vault_path() / note_path
            
        if not full_path.exists():
            return jsonify({"error": f"Note not found: {note_path}"}), 404
        
        try:
            content = ObsidianBase.read_file_content(full_path)
            connections = ObsidianBase.analyze_note_connections(content["content"])
            
            if include_backlinks:
                backlinks = []
                note_name = full_path.stem
                for file in ObsidianBase.get_vault_path().rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        file_content = ObsidianBase.read_file_content(file)
                        if file_content:
                            file_connections = ObsidianBase.analyze_note_connections(file_content["content"])
                            if note_name in file_connections["links"]:
                                backlinks.append(str(file.relative_to(ObsidianBase.get_vault_path())))
                connections["backlinks"] = backlinks
            
            return jsonify({"connections": connections }), 200
        
        except Exception as e:
            logger.error(f"Error analyzing connections: {e}")
            return jsonify({"error": str(e)}), 500
