import os
import logging
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json
import yaml
import re

logger = logging.getLogger('obsidian-server')

class ObsidianBase:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ObsidianBase, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
            
        self.vault_path = Path("D:/06_Project_Vi/extensions/vaults/CodeBase_Test")
        self.enable_semantic_search = False
        self.vector_store_path = Path(os.getenv('APPDATA')) / 'Claude' / 'obsidian_vectors'
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        try:
            self.setup_semantic_search()
            self.enable_semantic_search = True
            logger.info("Semantic search enabled")
        except Exception as e:
            logger.info(f"Semantic search not available: {e}")
            
        self.initialized = True

    def setup_semantic_search(self):
        """Initialize semantic search capabilities"""
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.indexed_files = []
        
        vector_file = self.vector_store_path / 'vectors.npy'
        files_file = self.vector_store_path / 'files.json'
        
        if vector_file.exists() and files_file.exists():
            vectors = np.load(str(vector_file))
            self.index.add(vectors)
            with open(files_file, 'r') as f:
                self.indexed_files = json.load(f)
        
        self.update_vector_index()

    def update_vector_index(self):
        """Update vector index with any new files"""
        try:
            for file in self.vault_path.rglob("*.md"):
                if not any(p.startswith('.') for p in file.parts):
                    relative_path = str(file.relative_to(self.vault_path))
                    if relative_path not in self.indexed_files:
                        content = self.read_file_content(file)
                        if content:
                            embedding = self.embeddings.encode([content])[0]
                            self.index.add(np.array([embedding]))
                            self.indexed_files.append(relative_path)
            
            if self.indexed_files:
                vectors = self.index.reconstruct_n(0, self.index.ntotal)
                np.save(str(self.vector_store_path / 'vectors.npy'), vectors)
                with open(self.vector_store_path / 'files.json', 'w') as f:
                    json.dump(self.indexed_files, f)
        except Exception as e:
            logger.error(f"Error updating vector index: {e}")

    def read_file_content(self, file_path: Path):
        """Read file content with frontmatter parsing"""
        try:
            content = file_path.read_text(encoding='utf-8')
            return self.parse_note(content)
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None

    def parse_note(self, content: str):
        """Parse note content and frontmatter"""
        try:
            if content.startswith('---'):
                _, frontmatter, content = content.split('---', 2)
                metadata = yaml.safe_load(frontmatter)
                return {
                    "metadata": metadata,
                    "content": content.strip(),
                    "tags": metadata.get("tags", [])
                }
            return {"content": content}
        except Exception as e:
            logger.error(f"Error parsing note: {e}")
            return {"content": content}

    def analyze_note_connections(self, content: str):
        """Analyze note connections and structure"""
        try:
            links = re.findall(r'\[\[(.*?)\]\]', content)
            tags = re.findall(r'#([\w-]+)', content)
            return {
                "links": links,
                "tags": tags
            }
        except Exception as e:
            logger.error(f"Error analyzing connections: {e}")
            return {"links": [], "tags": []}
