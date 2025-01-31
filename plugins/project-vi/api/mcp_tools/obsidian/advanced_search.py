from flask import jsonify, current_app
from flask_restx import Resource
from models import api, obsidian_search_model
from pathlib import Path
from utils.semantic_search import SemanticSearchManager
import logging

logger = logging.getLogger('obsidian')

@api.doc(
    methods=['POST'],
    description='Perform advanced search through Obsidian vault with multiple search types and options'
)
class AdvancedSearch(Resource):
    @api.expect(obsidian_search_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Search through Obsidian vault with advanced options"""
        try:
            data = api.payload
            vault_path = Path(current_app.config['VAULT_PATH'])
            
            results = []
            query = data['query']
            search_type = data.get('search_type', 'text')
            include_metadata = data.get('include_metadata', False)
            follow_links = data.get('follow_links', False)
            max_depth = data.get('max_depth', 1)

            semantic_manager = SemanticSearchManager(vault_path)
            
            if search_type == 'semantic' and semantic_manager.is_enabled:
                results = semantic_manager.search(query)
            else:
                for file in vault_path.rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        content = self._read_file_content(file)
                        if content and query.lower() in content['content'].lower():
                            result = {
                                'file': str(file.relative_to(vault_path)),
                                'preview': content['content'][:200] + '...'
                            }
                            if include_metadata:
                                result['metadata'] = content.get('metadata')
                            results.append(result)

                            if follow_links and max_depth > 0:
                                linked_results = self._follow_links(file, vault_path, max_depth)
                                results.extend(linked_results)

            return jsonify({'results': results}), 200

        except Exception as e:
            logger.error(f'Error in advanced search: {str(e)}')
            return jsonify({'error': str(e)}), 500

    def _read_file_content(self, file_path):
        """Read and parse file content"""
        try:
            content = file_path.read_text(encoding='utf-8')
            return {
                'content': content,
                'metadata': {}
            }
        except Exception as e:
            logger.error(f'Error reading file {file_path}: {e}')
            return None

    def _follow_links(self, file, vault_path, depth):
        """Follow file links up to specified depth"""
        return []
