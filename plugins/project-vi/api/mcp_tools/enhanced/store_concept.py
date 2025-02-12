from flask_restx import Resource
from flask import jsonify
import numpy as np
import logging
import json
from models import api, store_concept_model
from .base import MemoryBase

logger = logging.getLogger('enhanced-memory')

@api.doc(
    methods=['POST'],
    description='Store a concept with its embedding'
)
class StoreConcept(Resource, MemoryBase):
    @api.expect(store_concept_model)
    @api.response(201, 'Concept stored')
    @api.response(500, 'Internal Server Error')
    def post(self, content, metadata=None):
        try:
            if metadata is None:
                metadata = {}
                
            embedding = self.model.encode([content])[0]
            self.vectors = np.vstack([self.vectors, embedding])
            self.texts.append({
                "content": content,
                "metadata": metadata
            })
            
            np.save(str(self.vectors_path), self.vectors)
            with open(self.texts_path, 'w') as f:
                json.dump(self.texts, f)
            
            return jsonify({
                "message": f"Stored concept: {content[:50]}..."
            }), 201
            
        except Exception as e:
            logger.error(f"Error storing concept: {e}")
            return jsonify({"error": str(e)}), 500
