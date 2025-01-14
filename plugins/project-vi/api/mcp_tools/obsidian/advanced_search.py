from flask_restx import Resource
from flask import jsonify
import os
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
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
            vector_store_path = Path(os.getenv('APPDATA')) / 'Claude' / 'obsidian_vectors'
            results = []
            
            # Initialize semantic search if needed
            if search_type == "semantic":
                # Load existing vectors and files
                vectors = np.load(str(vector_store_path / 'vectors.npy'))
                with open(vector_store_path / 'files.json', 'r') as f:
                    indexed_files = json.load(f)
                
                embeddings = SentenceTransformer('all-MiniLM-L6-v2')
                dimension = 384
                index = faiss.IndexFlatL2(dimension)
                index.add(vectors)
                
                # Perform semantic search
                query_vector = embeddings.encode([query])[0]
                D, I = index.search(np.array([query_vector]), k=5)
                
                # Process results
                for idx, score in zip(I[0], D[0]):
                    if idx != -1:
                        file_path = vault_path / indexed_files[idx]
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            result = {
                                "file": indexed_files[idx],
                                "similarity": float(1 - score),
                                "preview": content[:200] + "..."
                            }
                            if include_metadata and content.startswith('---'):
                                try:
                                    _, frontmatter, _ = content.split('---', 2)
                                    result["metadata"] = yaml.safe_load(frontmatter)
                                except:
                                    pass
                            results.append(result)
                        except Exception as e:
                            logger.error(f"Error reading file {file_path}: {str(e)}")
                            continue
            
            else:
                # Implement text search (existing implementation)
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
