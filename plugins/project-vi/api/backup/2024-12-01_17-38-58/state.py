"""
State management for the LangGraph vault generator.
"""
import os
import logging
from typing import Dict, List, Optional, Sequence
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VaultMetadata(BaseModel):
    """Metadata for the vault and its contents."""
    tags: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Tags used in the vault, organized by category"
    )
    last_updated: Dict[str, str] = Field(
        default_factory=dict,
        description="Last update timestamps for files"
    )
    authors: List[str] = Field(
        default_factory=list,
        description="List of authors who have contributed"
    )

class FileMetadata(BaseModel):
    """Metadata for a specific file."""
    tags: List[str] = Field(
        default_factory=list,
        description="Tags associated with this file"
    )
    links: List[str] = Field(
        default_factory=list,
        description="Internal links in this file"
    )
    backlinks: List[str] = Field(
        default_factory=list,
        description="Files that link to this file"
    )
    last_updated: str = Field(
        default="",
        description="Timestamp of last update"
    )
    status: str = Field(
        default="draft",
        description="Current status of the file (draft, review, complete)"
    )

class VaultStructure(BaseModel):
    """Structure of the Obsidian vault."""
    root_path: str = Field(
        description="Root path of the vault"
    )
    directories: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Directory structure with list of files"
    )
    files: Dict[str, FileMetadata] = Field(
        default_factory=dict,
        description="Metadata for each file in the vault"
    )
    templates: Dict[str, str] = Field(
        default_factory=dict,
        description="Available templates in the vault"
    )

class VaultState(BaseModel):
    """Complete state of the Obsidian vault generation process."""
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Message history for the current operation"
    )
    current_file: Optional[str] = Field(
        default=None,
        description="Path of the file currently being processed"
    )
    vault_structure: VaultStructure = Field(
        description="Current structure of the vault"
    )
    metadata: VaultMetadata = Field(
        description="Global metadata for the vault"
    )
    operation_context: Dict[str, any] = Field(
        default_factory=dict,
        description="Additional context for the current operation"
    )

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True

def scan_directory(path: str) -> Dict[str, List[str]]:
    """Scan a directory and return its structure."""
    structure = {}
    for root, dirs, files in os.walk(path):
        # Skip .git and other hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Get relative path
        rel_path = os.path.relpath(root, path)
        if rel_path == '.':
            rel_path = ''
            
        # Store files for this directory
        structure[rel_path] = [f for f in files if f.endswith('.md')]
        
    return structure

def create_initial_state(vault_path: str) -> VaultState:
    """Create initial state from existing vault."""
    logger.info(f"Creating initial state for vault at: {vault_path}")
    
    # Scan the vault directory
    structure = scan_directory(vault_path)
    logger.info(f"Found {sum(len(files) for files in structure.values())} markdown files")
    
    # Create the state
    state = VaultState(
        vault_structure=VaultStructure(
            root_path=vault_path,
            directories=structure,
            files={},
            templates={}
        ),
        metadata=VaultMetadata(
            tags={},
            last_updated={},
            authors=[]
        )
    )
    
    return state