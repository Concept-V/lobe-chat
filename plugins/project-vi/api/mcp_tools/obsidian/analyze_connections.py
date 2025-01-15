from flask_restx import Resource
from flask import jsonify
import logging
from models import api, analyze_connections_model
from .base import ObsidianBase

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['POST'],
    description='Analyze connections between notes in the Obsidian vault'
)
class AnalyzeConnections(Resource, ObsidianBase):
    @api.expect(analyze_connections_model)
    @api.response(200, 'Success')
    @api.response(404, 'Note not found')
    @api.response(500, 'Internal Server Error')
    def post(self, note_path, include_backlinks=False):
        try:
            # Check if note exists
            note_path = self.vault_path / note_path
            if not note_path.exists():
                return jsonify({
                    "error": f"Note not found: {note_path}"
                }), 404
            
            # Read and parse note content
            content = self.read_file_content(note_path)
            if not content:
                return jsonify({
                    "error": "Could not read note content"
                }), 500
            
            # Analyze connections
            connections = self.analyze_note_connections(content["content"])
            
            # Add backlinks if requested
            if include_backlinks:
                backlinks = []
                note_name = note_path.stem
                for file in self.vault_path.rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        file_content = self.read_file_content(file)
                        if file_content:
                            file_connections = self.analyze_note_connections(file_content["content"])
                            if note_name in file_connections["links"]:
                                backlinks.append(str(file.relative_to(self.vault_path)))
                connections["backlinks"] = backlinks
            
            return jsonify(connections), 200
            
        except Exception as e:
            logger.error(f"Error analyzing connections: {e}")
            return jsonify({"error": str(e)}), 500
