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
def analyze_vault_structure(directories: Dict[str, List[str]]) -> str:
    """
    Analyze the current vault structure and provide insights.
    Args:
        directories: Dictionary mapping directory paths to lists of files
    Returns:
        String containing analysis of the vault structure
    """
    logger.info("Analyzing vault structure...")
    
    total_files = sum(len(files) for files in directories.values())
    total_dirs = len(directories)
    
    # Get directory details
    dir_details = []
    for dir_path, files in directories.items():
        if not dir_path:
            dir_path = "(root)"
        dir_details.append(f"- {dir_path}: {len(files)} files")
        # List a few example files
        if files:
            example_files = files[:3]
            dir_details.extend([f"  • {file}" for file in example_files])
            if len(files) > 3:
                dir_details.append(f"  • ... and {len(files) - 3} more files")
    
    return f"""
    Vault Analysis:
    Total Files: {total_files}
    Total Directories: {total_dirs}
    
    Directory Structure:
    {chr(10).join(dir_details)}
    """

@tool
def check_vault_health(directories: Dict[str, List[str]]) -> Dict:
    """
    Check the health of the vault structure.
    Args:
        directories: Dictionary mapping directory paths to lists of files
    Returns:
        Dictionary containing health check results
    """
    logger.info("Checking vault health...")
    
    issues = []
    
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
        issues.append(f"Found {len(non_md_files)} files without .md extension:")
        for file in non_md_files[:3]:  # Show first 3 examples
            issues.append(f"  • {file}")
        if len(non_md_files) > 3:
            issues.append(f"  • ... and {len(non_md_files) - 3} more")
    
    # Check for potential naming issues
    space_files = [f for f in file_names if ' ' in f]
    if space_files:
        issues.append(f"Found {len(space_files)} files with spaces in names:")
        for file in space_files[:3]:  # Show first 3 examples
            issues.append(f"  • {file}")
        if len(space_files) > 3:
            issues.append(f"  • ... and {len(space_files) - 3} more")
    
    # Check for numeric prefixes
    numeric_prefix_files = [f for f in file_names if any(f.startswith(str(i) + "_") for i in range(10))]
    if numeric_prefix_files:
        issues.append(f"Found {len(numeric_prefix_files)} files with numeric prefixes:")
        for file in numeric_prefix_files[:3]:  # Show first 3 examples
            issues.append(f"  • {file}")
        if len(numeric_prefix_files) > 3:
            issues.append(f"  • ... and {len(numeric_prefix_files) - 3} more")
    
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
        system="""You are an expert Obsidian vault organizer. Your role is to analyze and improve vault organization.

First, use analyze_vault_structure to understand the current structure.
Then, use check_vault_health to identify any issues.

After analysis:
1. Summarize the current vault structure
2. List any organizational issues found
3. Provide specific recommendations for improvement

If issues are found, clearly mark them with "ISSUES:" in your response.
Be specific and actionable in your recommendations."""
    )
    
    tools = [analyze_vault_structure, check_vault_health]
    return create_react_agent(model, tools)

def structure_node(state: VaultState) -> Dict:
    """Node for managing vault structure."""
    logger.info("Running structure node...")
    agent = create_structure_agent()
    
    # Get the directories from state
    directories = state.vault_structure.directories
    
    # Create initial message if none exists
    if not state.messages:
        state.messages = [
            HumanMessage(content="Please analyze the vault structure and provide insights about its organization.")
        ]
    
    logger.info("Invoking agent...")
    result = agent.invoke({
        "messages": state.messages,
        "directories": directories  # Pass directories directly as a tool input
    })
    
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