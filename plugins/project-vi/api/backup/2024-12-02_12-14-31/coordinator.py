"""
Coordinator agents for managing dynamic workload distribution.
"""
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WorkBatch:
    """Represents a batch of work to be processed."""
    id: str
    files: List[str]
    complexity: float
    dependencies: List[str] = None
    metadata: Dict = None

class WorkloadAnalyzer:
    """Analyzes workload and determines optimal batch sizes."""
    
    def __init__(self, max_batch_size: int = 10, complexity_threshold: float = 0.7):
        self.max_batch_size = max_batch_size
        self.complexity_threshold = complexity_threshold
    
    def calculate_complexity(self, file_path: str, content: str) -> float:
        """Calculate complexity score for a file."""
        # Basic complexity scoring
        score = 0.0
        
        # Size-based complexity
        score += len(content) / 10000  # Normalize by 10KB
        
        # Structure-based complexity
        if '```' in content:  # Code blocks
            score += 0.2
        if '[[' in content:  # Internal links
            score += 0.1 * content.count('[[')
        if '#' in content:  # Headers
            score += 0.1 * content.count('\n#')
            
        return min(score, 1.0)
    
    def create_batches(self, files: List[str], contents: Dict[str, str]) -> List[WorkBatch]:
        """Create work batches based on file complexity."""
        # Calculate complexities
        file_complexities = {
            f: self.calculate_complexity(f, contents.get(f, ''))
            for f in files
        }
        
        # Sort files by complexity
        sorted_files = sorted(files, key=lambda f: file_complexities[f], reverse=True)
        
        # Create batches
        batches = []
        current_batch = []
        current_complexity = 0.0
        batch_id = 1
        
        for file in sorted_files:
            file_complexity = file_complexities[file]
            
            # Start new batch if current would exceed thresholds
            if (len(current_batch) >= self.max_batch_size or 
                current_complexity + file_complexity > self.complexity_threshold):
                if current_batch:
                    batches.append(WorkBatch(
                        id=f"batch_{batch_id}",
                        files=current_batch.copy(),
                        complexity=current_complexity
                    ))
                    batch_id += 1
                    current_batch = []
                    current_complexity = 0.0
            
            current_batch.append(file)
            current_complexity += file_complexity
        
        # Add final batch
        if current_batch:
            batches.append(WorkBatch(
                id=f"batch_{batch_id}",
                files=current_batch,
                complexity=current_complexity
            ))
        
        return batches

class CoordinatorAgent:
    """Manages the distribution and coordination of work across agent pools."""
    
    def __init__(self, model_name: str = "claude-3-sonnet-20240229"):
        self.model = ChatAnthropic(
            model=model_name,
            temperature=0
        ).bind(
            system="""You are the coordinator agent responsible for managing a distributed documentation processing system.
Your role is to:
1. Analyze incoming work and determine optimal distribution
2. Monitor agent pool performance
3. Adjust resource allocation based on workload
4. Ensure work dependencies are respected
5. Handle any coordination issues that arise

Provide clear, actionable coordination decisions."""
        )
        self.workload_analyzer = WorkloadAnalyzer()
        
    def create_agent(self):
        """Create the coordinator agent."""
        tools = [
            self._analyze_workload,
            self._monitor_progress,
            self._adjust_resources
        ]
        return create_react_agent(self.model, tools)
    
    def _analyze_workload(self, files: List[str], contents: Dict[str, str]) -> Dict:
        """Analyze workload and create optimal work distribution."""
        batches = self.workload_analyzer.create_batches(files, contents)
        return {
            "total_batches": len(batches),
            "batch_details": [
                {
                    "id": b.id,
                    "size": len(b.files),
                    "complexity": b.complexity
                }
                for b in batches
            ]
        }
    
    def _monitor_progress(self, batch_statuses: Dict[str, str]) -> Dict:
        """Monitor progress of work across agent pools."""
        completed = sum(1 for status in batch_statuses.values() if status == "completed")
        in_progress = sum(1 for status in batch_statuses.values() if status == "in_progress")
        pending = sum(1 for status in batch_statuses.values() if status == "pending")
        
        return {
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "total": len(batch_statuses)
        }
    
    def _adjust_resources(self, current_metrics: Dict) -> Dict:
        """Adjust resource allocation based on current metrics."""
        recommendations = []
        
        # Check for bottlenecks
        if current_metrics.get("queue_size", 0) > 10:
            recommendations.append("Increase analysis agents")
        if current_metrics.get("pending_transforms", 0) > 5:
            recommendations.append("Increase transform agents")
        
        return {
            "recommendations": recommendations,
            "current_load": current_metrics.get("load", "normal"),
            "suggested_actions": [
                action for action in recommendations if action
            ]
        }