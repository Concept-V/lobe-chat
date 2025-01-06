"""
Graph orchestration for the LangGraph vault generator.
"""
import logging
from typing import Dict, Literal
from langgraph.graph import StateGraph, END

from .state import (
    VaultState, 
    create_initial_state, 
    ValidationConfig,
    OperationContext
)
from .agents import structure_node, should_continue

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_vault_graph() -> StateGraph:
    """Create the main graph for vault analysis."""
    logger.info("Creating vault analysis graph...")
    
    # Initialize the graph
    workflow = StateGraph(VaultState)
    
    # Add the structure agent node
    workflow.add_node("structure", structure_node)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "structure",
        should_continue,
        {
            "structure": "structure",  # Loop back if issues found
            END: END
        }
    )
    
    # Set the entry point
    workflow.set_entry_point("structure")
    
    # Compile the graph
    return workflow.compile()

class VaultOrchestrator:
    """High-level orchestrator for vault operations."""
    
    def __init__(self, vault_path: str):
        """Initialize the orchestrator."""
        logger.info(f"Initializing VaultOrchestrator for path: {vault_path}")
        self.state = create_initial_state(vault_path)
        self.graph = create_vault_graph()
    
    def validate_vault(
        self, 
        scope: Literal["all", "links", "metadata", "structure"] = "all"
    ) -> VaultState:
        """Validate the vault's integrity."""
        logger.info(f"Validating vault with scope: {scope}")
        
        # Update operation context with validation config
        self.state.operation_context = OperationContext(
            operation_type="validate",
            validation_config=ValidationConfig(scope=scope)
        )
        
        # Run the graph
        result = self.graph.invoke(self.state)
        
        # Update state with results
        self.state.messages.extend(result["messages"])
        
        return self.state
    
    def get_vault_status(self) -> Dict:
        """Get a comprehensive status report of the vault."""
        logger.info("Getting vault status...")
        
        status = {
            "total_files": sum(len(files) for files in self.state.vault_structure.directories.values()),
            "total_directories": len(self.state.vault_structure.directories),
            "total_tags": len(self.state.metadata.tags),
            "last_operation": self.state.operation_context.operation_type,
            "health_metrics": {}
        }
        
        # Get health metrics from the last validation if available
        if self.state.messages:
            last_message = self.state.messages[-1]
            status["health_metrics"] = {
                "message": last_message.content,
                "timestamp": self.state.metadata.last_updated.get("last_validation")
            }
        
        return status