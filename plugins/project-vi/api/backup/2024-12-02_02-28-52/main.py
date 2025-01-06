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
    
    # First, validate the current vault structure
    print("Validating current vault structure...")
    state = orchestrator.validate_vault(scope="all")
    
    # Get and print the vault status
    status = orchestrator.get_vault_status()
    print("\nCurrent Vault Status:")
    print(f"Total Files: {status['total_files']}")
    print(f"Total Directories: {status['total_directories']}")
    print(f"Total Tags: {status['total_tags']}")
    
    # Print health metrics
    print("\nHealth Metrics:")
    for key, value in status['health_metrics'].items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()