import os
import logging
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import json

logger = logging.getLogger('enhanced-memory')

class MemoryBase:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryBase, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
            
        self.base_path = Path('./api/mcp_tools/store')
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize vector store
        logger.info("Initializing vector store...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectors_path = self.base_path / 'vectors.npy'
        self.texts_path = self.base_path / 'texts.json'
        self.init_vectors()
        
        self.initialized = True

    def init_vectors(self):
        if self.vectors_path.exists() and self.texts_path.exists():
            logger.info("Loading existing vectors...")
            self.vectors = np.load(str(self.vectors_path))
            with open(self.texts_path) as f:
                self.texts = json.load(f)
        else:
            logger.info("Creating new vector store...")
            self.vectors = np.array([], dtype=np.float32).reshape(0, 384)
            self.texts = []
