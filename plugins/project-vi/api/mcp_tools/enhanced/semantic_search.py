from flask_restx import Resource
from flask import jsonify
import numpy as np
import logging
from models import api, semantic_search_model
from .base import MemoryBase

logger = logging.getLogger('enhanced-memory')

@api.doc(
    methods=['POST'],
    description='Search using semantic similarity'
)
class SemanticSearch(Resource, MemoryBase):
    @api.expect(semantic_search_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self, query, limit=5):
        try:
            if len(self.vectors) == 0:
                return jsonify({ "message": "No documents indexed yet for semantic search." }), 200
                
            query_vector = self.model.encode([query])[0]
            similarities = np.dot(self.vectors, query_vector)
            top_k = np.argsort(similarities)[-limit:][::-1]
            
            results = [
                {
                    "text": self.texts[i],
                    "similarity": float(similarities[i])
                }
                for i in top_k
            ]
            
            return jsonify({"results": results}), 200
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return jsonify({"error": str(e)}), 500
