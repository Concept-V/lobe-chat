from flask_restx import Resource
from flask import jsonify
import os
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from models import api, advanced_search_model

logger = logging.getLogger('obsidian-server')

@api.doc(
    methods=['POST'],
    description='Advanced search functionality for Obsidian vault',
)
class AdvancedSearch(Resource):
    @api.expect(advanced_search_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self, query, search_type='text', include_metadata=False, follow_links=False, max_depth=1):
        try:
            vault_path = Path("D:/06_Project_Vi/extensions/vaults/CodeBase_Test")
            results = []
            
            # Initialize semantic search if needed
            if search_type == "semantic":
                embeddings = SentenceTransformer('all-MiniLM-L6-v2')
                dimension = 384
                index = faiss.IndexFlatL2(dimension)
                
                # Perform semantic search
                query_vector = embeddings.encode([query])[0]
                D, I = index.search(np.array([query_vector]), k=5)
                # ... implement semantic search logic
            
            else:
                # Implement text search
                query = query.lower()
                for file in vault_path.rglob("*.md"):
                    if not any(p.startswith('.') for p in file.parts):
                        try:
                            content = file.read_text(encoding='utf-8')
                            if query in content.lower():
                                results.append({
                                    "file": str(file.relative_to(vault_path)),
                                    "preview": content[:200] + "..."
                                })
                        except Exception as e:
                            logger.error(f"Error reading file {file}: {str(e)}")
                            continue
            
            return jsonify({"results": results}), 200
            
        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            return jsonify({"error": str(e)}), 500
        