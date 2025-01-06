"""
Agent nodes for the LangGraph vault generator.
"""
import logging
import os
from typing import Dict, List
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

from .state import VaultState

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define tools for the structure agent
@tool
def analyze_vault_structure(state: VaultState) -> str:
    """Analyze the current vault structure and provide insights."""
    logger.info("Analyzing vault structure...")
    
    total_files = sum(len(files) for files in state.vault_structure.directories.values())
    total_dirs = len(state.vault_structure.directories)
    
    return f"""
    Vault Analysis:
    - Total files: {total_files}
    - Total directories: {total_dirs}
    - Root path: {state.vault_structure.root_path}
    """

@tool
def check_vault_health(state: VaultState) -> Dict:
    """Check the health of the vault."""
    logger.info("Checking vault health...")
    
    issues = []
    
    # Check for empty directories
    for dir_path, files in state.vault_structure.directories.items():
        if not files:
            issues.append(f"Empty directory: {dir_path}")
    
    # Check for consistency
    if not state.vault_structure.files:
        issues.append("No file metadata available")
    
    return {
        "healthy": len(issues) == 0,
        "issues": issues
    }

# Create the agents using prebuilt ReAct agent with Claude
def create_structure_agent():
    """Create the structure management agent."""
    # Create the model with system message
    model = ChatAnthropic(
        model="claude-3.5-sonnet-20240229",
        temperature=0
    ).bind(
        system="""You are an expert Obsidian vault organizer. Your role is to:
1. Analyze vault structure for optimal organization
2. Identify potential issues or improvements
3. Maintain consistent directory structure
4. Handle file organization

Use the provided tools to analyze and validate the vault structure.
Provide clear, actionable insights about the vault's organization."""
    )
    
    tools = [analyze_vault_structure, check_vault_health]
    return create_react_agent(model, tools)

def structure_node(state: VaultState) -> Dict:
    """Node for managing vault structure."""
    logger.info("Running structure node...")
    agent = create_structure_agent()
    
    # Create initial message if none exists
    if not state.messages:
        state.messages = [
            HumanMessage(content="Please analyze the current vault structure and provide insights about its organization.")
        ]
    
    result = agent.invoke(state)
    return {"messages": result["messages"]}

# Edge functions
def should_continue(state: VaultState) -> str:
    """Determine if processing should continue."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if there are any issues that need addressing
    if "issues" in last_message.content.lower():
        return "structure"
    return "END"