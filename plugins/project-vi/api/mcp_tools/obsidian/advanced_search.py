from flask_restx import Resource
from flask import jsonify
import numpy as np
from models import api, advanced_search_model
from .base import ObsidianBase
import logging

logger = logging.getLogger('obsidian')

@api.doc(
    methods=['POST'],
    description='Advanced search with text or semantic options'
)
class AdvancedSearch(Resource):
    @api.expect(advanced_search_model)
    @api.response(200, 'Success')
    @api.response(400, 'Invalid vault path')
    @api.response(500, 'Internal Server Error')
    def post(self, vault_path, query, search_type='text', include_metadata=False, follow_links=False, max_depth=1):
        
        if not vault_path:
            return jsonify({"error": "Invalid vault path"}), 400
        
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        ObsidianBase.set_vault_path(vault_path)

        try:
            results = []
            
            if search_type == "semantic" and ObsidianBase.is_semantic_search_enabled():
                # Semantic search
                query_vector = ObsidianBase.get_embeddings().encode([query])[0]
                D, I = ObsidianBase.get_index().search(np.array([query_vector]), k=5)
                
                for idx, score in zip(I[0], D[0]):
                    if idx != -1:
                        file_path = ObsidianBase.get_vault_path() / ObsidianBase.get_indexed_files()[idx]
                        content = ""
                        content = ObsidianBase.read_file_content(file_path)

                        results.append({
                            "file": ObsidianBase.get_indexed_files()[idx],
                            "similarity": float(1 - score),
                            "content": content.get("content", "")[:200] + "...",
                            "metadata": content.get("metadata") if include_metadata else None
                        })
            else:
                # Text search
                query = query.lower()
                for file in ObsidianBase.get_vault_path().rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        content = ObsidianBase.read_file_content(file)
                        if content and query in content["content"].lower():
                            result = {
                                "file": str(file.relative_to(ObsidianBase.get_vault_path())),
                                "preview": content["content"][:200] + "..."
                            }
                            if include_metadata:
                                result["metadata"] = content.get("metadata")
                            results.append(result)

                            # Follow links if requested
                            if follow_links and max_depth > 0:
                                connections = ObsidianBase.analyze_note_connections(content["content"])
                                for link in connections["links"]:
                                    linked_file = ObsidianBase.get_vault_path() / (link + ".md")
                                    if linked_file.exists():
                                        linked_content = ""
                                        linked_content = ObsidianBase.read_file_content(linked_file)
                                        if linked_content:
                                            results.append({
                                                "file": link + ".md",
                                                "preview": linked_content["content"][:200] + "...",
                                                "connection": "linked from " + str(file.relative_to(ObsidianBase.get_vault_path()))
                                            })

            return jsonify({"results": results}), 200
        
        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            return jsonify({"error": str(e)}), 500
