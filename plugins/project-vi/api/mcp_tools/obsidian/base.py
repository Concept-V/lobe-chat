import os
import logging
import re
import yaml
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json
from typing import Optional

logger = logging.getLogger('obsidian')

class ObsidianBase:
    _vault_path = None
    _embeddings = None
    _index = None
    _indexed_files = []
    _enable_semantic_search = False
    _vector_store_path = Path('./api/mcp_tools/store/obsidian_vectors')

    @classmethod
    def set_vault_path(cls, path: str):
        """Set the vault path before initializing"""
        cls._vault_path = Path(path)
        if not cls._vault_path.exists():
            raise ValueError(f"Vault path does not exist: {cls._vault_path}")
        cls._vector_store_path.mkdir(parents=True, exist_ok=True)
        cls._initialize()

    @classmethod
    def _initialize(cls):
        """Initialize the class"""
        try:
            cls._setup_semantic_search()
            cls._enable_semantic_search = True
            logger.info("Semantic search enabled")
        except Exception as e:
            logger.info(f"Semantic search not available: {e}")

    @classmethod
    def _setup_semantic_search(cls):
        """Initialize semantic search capabilities"""
        cls._embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        cls._index = faiss.IndexFlatL2(384)

        vector_file = cls._vector_store_path / 'vectors.npy'
        files_file = cls._vector_store_path / 'files.json'

        if vector_file.exists() and files_file.exists():
            vectors = np.load(str(vector_file))
            cls._index.add(vectors)
            with open(files_file, 'r') as f:
                cls._indexed_files = json.load(f)

        cls._update_vector_index()

    @classmethod
    def _update_vector_index(cls):
        """Update vector index with any new files"""
        try:
            for file in cls._vault_path.rglob("*.md"):
                if not any(p.startswith('.') for p in file.parts):
                    relative_path = str(file.relative_to(cls._vault_path))
                    if relative_path not in cls._indexed_files:
                        content = cls.read_file_content(file)
                        if content:
                            embedding = cls._embeddings.encode([content])[0]
                            cls._index.add(np.array([embedding]))
                            cls._indexed_files.append(relative_path)

            if cls._indexed_files:
                vectors = cls._index.reconstruct_n(0, cls._index.ntotal)
                np.save(str(cls._vector_store_path / 'vectors.npy'), vectors)
                with open(cls._vector_store_path / 'files.json', 'w') as f:
                    json.dump(cls._indexed_files, f)
        except Exception as e:
            logger.error(f"Error updating vector index: {e}")

    @classmethod
    def read_file_content(cls, file_path: Path) -> Optional[str]:
        """Read file content with frontmatter parsing"""
        try:
            content = file_path.read_text(encoding='utf-8')
            return cls.parse_note(content)
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None

    @classmethod
    def parse_note(cls, content: str) -> dict:
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

    @classmethod
    def analyze_note_connections(cls, content: str) -> dict:
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

    @classmethod
    def get_vault_path(cls) -> Path:
        """Get the vault path"""
        return cls._vault_path
    
    @classmethod
    def get_embeddings(cls):
        """Get the embeddings model (if initialized)"""
        return cls._embeddings

    @classmethod
    def get_index(cls):
        """Get the FAISS index object"""
        return cls._index
    
    @classmethod
    def get_indexed_files(cls) -> list:
        """Public method to get the list of indexed files"""
        return cls._indexed_files

    @classmethod
    def is_semantic_search_enabled(cls) -> bool:
        """Check if semantic search is enabled"""
        return cls._enable_semantic_search

