"""
Agent nodes for the LangGraph vault generator.
"""
import logging
import os
from typing import Dict, List, Literal
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.graph import END

from .state import VaultState

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define tools for the structure agent
@tool
def analyze_vault_structure(state: Dict) -> str:
    """
    Analyze the current vault structure and provide insights.
    Args:
        state: Dictionary containing vault structure information
    Returns:
        String containing analysis of the vault structure
    """
    logger.info("Analyzing vault structure...")
    logger.info(f"Received state: {state}")
    
    directories = state.get("directories", {})
    total_files = sum(len(files) for files in directories.values())
    total_dirs = len(directories)
    
    # Get directory details
    dir_details = []
    for dir_path, files in directories.items():
        if not dir_path:
            dir_path = "(root)"
        dir_details.append(f"- {dir_path}: {len(files)} files")
    
    return f"""
    Vault Analysis:
    Total Files: {total_files}
    Total Directories: {total_dirs}
    
    Directory Breakdown:
    {chr(10).join(dir_details)}
    """

@tool
def check_vault_health(state: Dict) -> Dict:
    """
    Check the health of the vault structure.
    Args:
        state: Dictionary containing vault structure information
    Returns:
        Dictionary containing health check results
    """
    logger.info("Checking vault health...")
    logger.info(f"Received state: {state}")
    
    issues = []
    directories = state.get("directories", {})
    
    # Check for empty directories
    for dir_path, files in directories.items():
        if not files:
            issues.append(f"Empty directory found: {dir_path or '(root)'}")
    
    # Check for potential naming inconsistencies
    file_names = []
    for files in directories.values():
        file_names.extend(files)
    
    # Check for files without .md extension
    non_md_files = [f for f in file_names if not f.endswith('.md')]
    if non_md_files:
        issues.append(f"Found {len(non_md_files)} files without .md extension")
    
    # Check for potential naming issues
    space_files = [f for f in file_names if ' ' in f]
    if space_files:
        issues.append(f"Found {len(space_files)} files with spaces in names")
    
    return {
        "healthy": len(issues) == 0,
        "issues": issues,
        "total_files": sum(len(files) for files in directories.values()),
        "total_directories": len(directories)
    }

# Create the agents using prebuilt ReAct agent with Claude
def create_structure_agent():
    """Create the structure management agent."""
    # Create the model with system message
    model = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        temperature=0
    ).bind(
        system="""You are an expert Obsidian vault organizer. Your role is to:
1. Analyze vault structure for optimal organization
2. Identify potential issues and improvements
3. Maintain consistent directory structure
4. Handle file organization

Use the provided tools to analyze and validate the vault structure.
First, use analyze_vault_structure to get an overview.
Then, use check_vault_health to identify any issues.

Provide clear, actionable insights about the vault's organization.
If any issues are found, clearly state them as "ISSUES:" in your response."""
    )
    
    tools = [analyze_vault_structure, check_vault_health]
    return create_react_agent(model, tools)

def structure_node(state: VaultState) -> Dict:
    """Node for managing vault structure."""
    logger.info("Running structure node...")
    agent = create_structure_agent()
    
    # Convert state to dict for tools
    state_dict = {
        "directories": state.vault_structure.directories,
        "root_path": state.vault_structure.root_path
    }
    
    # Create initial message if none exists
    if not state.messages:
        state.messages = [
            HumanMessage(content="Please analyze the vault structure and provide insights about its organization.")
        ]
    
    # Create the input for the agent with both messages and state
    agent_input = {
        "messages": state.messages,
        "input": state_dict  # This is the key change - providing state as input
    }
    
    logger.info(f"Invoking agent with input: {agent_input}")
    result = agent.invoke(agent_input)
    return {"messages": result["messages"]}

# Edge functions
def should_continue(state: VaultState) -> Literal["structure", "END"]:
    """Determine if processing should continue."""
    logger.info("Checking if processing should continue...")
    
    if not state.messages:
        logger.info("No messages found, ending processing...")
        return "END"
        
    last_message = state.messages[-1]
    
    # Check if there are any issues that need addressing
    if hasattr(last_message, 'content') and "ISSUES:" in last_message.content.upper():
        logger.info("Found issues, continuing processing...")
        return "structure"
    
    logger.info("No issues found, ending processing...")
    return "END"