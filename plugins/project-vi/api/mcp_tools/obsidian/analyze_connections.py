from flask import jsonify, current_app
from flask_restx import Resource
from models.base import api
from models.obsidian import obsidian_connections_model
from pathlib import Path
import re
import logging 

logger = logging.getLogger('obsidian')

@api.doc(
    methods=['POST'],
    description='Analyze connections between notes including links, tags, and backlinks'
)
class AnalyzeConnections(Resource):
    @api.expect(obsidian_connections_model)
    @api.response(200, 'Success')
    @api.response(404, 'Note not found')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Analyze connections between notes"""
        try:
            data = api.payload
            vault_path = Path(current_app.config['VAULT_PATH'])
            note_path = vault_path / data['note_path']
            include_backlinks = data.get('include_backlinks', False)

            if not note_path.exists():
                return jsonify({
                    'error': f'Note not found: {data["note_path"]}'
                }), 404

            content = self._read_file_content(note_path)
            if not content:
                return jsonify({
                    'error': 'Could not read note content'
                }), 500

            connections = self._analyze_connections(content['content'])

            if include_backlinks:
                backlinks = self._find_backlinks(note_path, vault_path)
                connections['backlinks'] = backlinks

            return jsonify(connections), 200

        except Exception as e:
            logger.error(f'Error analyzing connections: {str(e)}')
            return jsonify({'error': str(e)}), 500

    def _analyze_connections(self, content):
        """Analyze note connections and structure"""
        try:
            links = re.findall(r'\[\[(.*?)\]\]', content)
            tags = re.findall(r'#([\w-]+)', content)
            return {
                'links': links,
                'tags': tags
            }
        except Exception as e:
            logger.error(f'Error analyzing connections: {e}')
            return {'links': [], 'tags': []}
