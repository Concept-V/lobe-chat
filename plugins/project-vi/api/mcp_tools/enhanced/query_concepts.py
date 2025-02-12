from flask_restx import Resource
from flask import jsonify
import numpy as np
import logging
from models import api, query_concepts_model
from .base import MemoryBase

logger = logging.getLogger('enhanced-memory')

@api.doc(
    methods=['POST'],
    description='Query stored concepts'
)
class QueryConcepts(Resource, MemoryBase):
    @api.expect(query_concepts_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self, query, limit=5):
        try:
            if len(self.vectors) == 0:
                return jsonify({"message": "No concepts stored yet."}), 200
            
            query_vector = self.model.encode([query])[0]
            similarities = np.dot(self.vectors, query_vector)
            top_k = np.argsort(similarities)[-limit:][::-1]
            
            results = [
                {
                    "content": self.texts[i]["content"],
                    "metadata": self.texts[i]["metadata"],
                    "similarity": float(similarities[i])
                }
                for i in top_k
            ]
            
            return jsonify({"results": results}), 200
            
        except Exception as e:
            logger.error(f"Error querying concepts: {e}")
            return jsonify({"error": str(e)}), 500
