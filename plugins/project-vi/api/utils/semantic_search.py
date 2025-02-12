from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger('search')

class SemanticSearchManager:
    def __init__(self, vault_path: Path):
        """Initialize semantic search capabilities with a given vault path"""
        self.vault_path = vault_path
        self.is_enabled = False
        self.vector_store_path = Path('data/vector_store')
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Initialize sentence transformer model
            self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
            self.dimension = 384  # Dimension of the model's embeddings
            self.index = faiss.IndexFlatL2(self.dimension)
            self.indexed_files = []
            
            # Load existing vectors if any
            self._load_existing_vectors()
            
            # Index any new files
            self.update_vector_index()
            self.is_enabled = True
            logger.info("Semantic search initialized successfully")
            
        except Exception as e:
            logger.error(f"Could not initialize semantic search: {e}")
            self.is_enabled = False

    def _load_existing_vectors(self):
        """Load existing vector index and file mappings"""
        vector_file = self.vector_store_path / 'vectors.npy'
        files_file = self.vector_store_path / 'files.json'
        
        if vector_file.exists() and files_file.exists():
            try:
                vectors = np.load(str(vector_file))
                self.index.add(vectors)
                with open(files_file, 'r') as f:
                    self.indexed_files = json.load(f)
                logger.info(f"Loaded {len(self.indexed_files)} existing vector embeddings")
            except Exception as e:
                logger.error(f"Error loading existing vectors: {e}")

    def update_vector_index(self):
        """Update vector index with any new files"""
        try:
            new_files = []
            new_vectors = []
            
            for file in self.vault_path.rglob("*.md"):
                if not any(p.startswith('.') for p in file.parts):
                    relative_path = str(file.relative_to(self.vault_path))
                    if relative_path not in self.indexed_files:
                        content = self._read_file_content(file)
                        if content:
                            embedding = self.embeddings.encode([content])[0]
                            new_vectors.append(embedding)
                            new_files.append(relative_path)
            
            if new_vectors:
                self.index.add(np.array(new_vectors))
                self.indexed_files.extend(new_files)
                
                # Save updated index
                self._save_index()
                logger.info(f"Added {len(new_files)} new files to vector index")
                
        except Exception as e:
            logger.error(f"Error updating vector index: {e}")

    def _save_index(self):
        """Save current index state to disk"""
        try:
            vectors = faiss.extract_vectors(self.index)
            np.save(str(self.vector_store_path / 'vectors.npy'), vectors)
            with open(self.vector_store_path / 'files.json', 'w') as f:
                json.dump(self.indexed_files, f)
        except Exception as e:
            logger.error(f"Error saving index: {e}")

    def _read_file_content(self, file_path: Path) -> Optional[str]:
        """Read and preprocess file content"""
        try:
            content = file_path.read_text(encoding='utf-8')
            # Simple preprocessing - you might want to add more sophisticated processing
            return content.strip()
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Search for semantically similar documents
        
        Args:
            query: Search query string
            k: Number of results to return
            
        Returns:
            List of dictionaries containing search results with similarity scores
        """
        try:
            if not self.is_enabled:
                logger.warning("Semantic search is not enabled")
                return []
                
            query_vector = self.embeddings.encode([query])[0]
            distances, indices = self.index.search(np.array([query_vector]), k)
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx != -1:  # Valid index
                    file_path = self.vault_path / self.indexed_files[idx]
                    preview = self._get_preview(file_path)
                    results.append({
                        'file': self.indexed_files[idx],
                        'similarity': float(1 - distance),  # Convert distance to similarity score
                        'preview': preview
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error during semantic search: {e}")
            return []

    def _get_preview(self, file_path: Path, preview_length: int = 200) -> str:
        """Get a preview of the file content"""
        try:
            content = self._read_file_content(file_path)
            if content:
                return content[:preview_length] + "..."
            return ""
        except Exception as e:
            logger.error(f"Error getting preview for {file_path}: {e}")
            return ""
