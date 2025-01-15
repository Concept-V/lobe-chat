from flask_restx import Resource
from flask import jsonify
import logging
import numpy as np
from models import api, advanced_search_model
from .base import ObsidianBase

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['POST'],
    description='Advanced search functionality for Obsidian vault'
)
class AdvancedSearch(Resource, ObsidianBase):
    @api.expect(advanced_search_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self, query, search_type='text', include_metadata=False, follow_links=False, max_depth=1):
        try:
            results = []
            
            if search_type == "semantic" and self.enable_semantic_search:
                # Semantic search
                query_vector = self.embeddings.encode([query])[0]
                D, I = self.index.search(np.array([query_vector]), k=5)
                for idx, score in zip(I[0], D[0]):
                    if idx != -1:
                        file_path = self.vault_path / self.indexed_files[idx]
                        content = self.read_file_content(file_path)
                        results.append({
                            "file": self.indexed_files[idx],
                            "similarity": float(1 - score),
                            "content": content.get("content", "")[:200] + "...",
                            "metadata": content.get("metadata") if include_metadata else None
                        })
            else:
                # Text search
                query = query.lower()
                for file in self.vault_path.rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        content = self.read_file_content(file)
                        if content and query in content["content"].lower():
                            result = {
                                "file": str(file.relative_to(self.vault_path)),
                                "preview": content["content"][:200] + "..."
                            }
                            if include_metadata:
                                result["metadata"] = content.get("metadata")
                            results.append(result)

                            # Follow links if requested
                            if follow_links and max_depth > 0:
                                connections = self.analyze_note_connections(content["content"])
                                for link in connections["links"]:
                                    linked_file = self.vault_path / (link + ".md")
                                    if linked_file.exists():
                                        linked_content = self.read_file_content(linked_file)
                                        if linked_content:
                                            results.append({
                                                "file": link + ".md",
                                                "preview": linked_content["content"][:200] + "...",
                                                "connection": "linked from " + str(file.relative_to(self.vault_path))
                                            })
            
            return jsonify({"results": results}), 200
            
        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            return jsonify({"error": str(e)}), 500
