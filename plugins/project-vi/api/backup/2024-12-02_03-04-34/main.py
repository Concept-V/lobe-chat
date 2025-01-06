"""
Main entry point for the LangGraph Vault Generator.
"""
import os
from typing import Dict, List
from implementation.orchestration import VaultOrchestrator
from implementation.state import create_initial_state

def main():
    # Initialize the orchestrator with the LangGraph vault path
    vault_path = "C:\\Users\\Tim\\Documents\\Finances\\Vi\\project vi\\Extenstions\\Vault\\Langgraph"
    orchestrator = VaultOrchestrator(vault_path)
    
    # Analyze the vault and plan transformation
    print("Analyzing vault and planning transformation...")
    state = orchestrator.analyze_and_plan_transformation(scope="all")
    
    # Get and print the analysis results
    status = orchestrator.get_vault_status()
    print("\nVault Analysis Results:")
    print(f"Total Files: {status['total_files']}")
    print(f"Total Directories: {status['total_directories']}")
    
    if 'analysis_results' in status:
        print("\nAnalysis and Transformation Plan:")
        print(status['analysis_results']['message'])

if __name__ == "__main__":
    main()