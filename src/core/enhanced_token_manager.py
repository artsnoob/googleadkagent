"""
Enhanced Token Manager with predictive capabilities and intelligent context management.
"""
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from collections import deque
import numpy as np
from datetime import datetime
import json
from pathlib import Path

from .token_manager import TokenManager


@dataclass
class TokenUsagePattern:
    """Pattern of token usage for a specific task type."""
    task_type: str
    avg_tokens: float
    std_deviation: float
    sample_count: int
    last_updated: datetime


@dataclass
class ContextPriority:
    """Priority information for context items."""
    content_hash: str
    relevance_score: float
    recency_score: float
    reference_count: int
    timestamp: datetime
    
    @property
    def priority_score(self) -> float:
        """Calculate overall priority score."""
        # Weighted combination of factors
        return (self.relevance_score * 0.5 + 
                self.recency_score * 0.3 + 
                min(self.reference_count / 10, 1.0) * 0.2)


class SmartTokenManager(TokenManager):
    """Enhanced token manager with predictive and prioritization capabilities."""
    
    def __init__(self, model_name: str, max_context_tokens: int = 120000,
                 learning_file: Optional[Path] = None):
        super().__init__(model_name, max_context_tokens)
        
        self.usage_patterns: Dict[str, TokenUsagePattern] = {}
        self.context_priorities: Dict[str, ContextPriority] = {}
        self.task_history = deque(maxlen=100)  # Keep last 100 tasks
        self.learning_file = learning_file or Path("./agent_files/token_patterns.json")
        
        self._load_patterns()
    
    def _load_patterns(self):
        """Load learned token usage patterns."""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r') as f:
                    data = json.load(f)
                    for pattern_data in data.get('patterns', []):
                        pattern = TokenUsagePattern(
                            task_type=pattern_data['task_type'],
                            avg_tokens=pattern_data['avg_tokens'],
                            std_deviation=pattern_data['std_deviation'],
                            sample_count=pattern_data['sample_count'],
                            last_updated=datetime.fromisoformat(pattern_data['last_updated'])
                        )
                        self.usage_patterns[pattern.task_type] = pattern
            except Exception:
                pass
    
    def _save_patterns(self):
        """Save learned patterns for persistence."""
        try:
            self.learning_file.parent.mkdir(parents=True, exist_ok=True)
            patterns_data = []
            
            for pattern in self.usage_patterns.values():
                patterns_data.append({
                    'task_type': pattern.task_type,
                    'avg_tokens': pattern.avg_tokens,
                    'std_deviation': pattern.std_deviation,
                    'sample_count': pattern.sample_count,
                    'last_updated': pattern.last_updated.isoformat()
                })
            
            with open(self.learning_file, 'w') as f:
                json.dump({'patterns': patterns_data}, f, indent=2)
        except Exception:
            pass
    
    def predict_token_usage(self, task: str) -> Tuple[int, int]:
        """
        Predict token usage for a task.
        
        Returns:
            Tuple of (expected_tokens, confidence_interval)
        """
        task_type = self._classify_task(task)
        
        if task_type in self.usage_patterns:
            pattern = self.usage_patterns[task_type]
            # Use 95% confidence interval (2 standard deviations)
            expected = int(pattern.avg_tokens)
            confidence_interval = int(pattern.std_deviation * 2)
            return expected, confidence_interval
        
        # Default prediction based on task length
        base_estimate = len(task) * 10  # Rough estimate
        return base_estimate, base_estimate // 2
    
    def _classify_task(self, task: str) -> str:
        """Classify task into categories for pattern matching."""
        task_lower = task.lower()
        
        # Simple classification based on keywords
        if any(word in task_lower for word in ['search', 'find', 'research']):
            return 'search'
        elif any(word in task_lower for word in ['create', 'write', 'generate']):
            return 'creation'
        elif any(word in task_lower for word in ['analyze', 'process', 'calculate']):
            return 'analysis'
        elif any(word in task_lower for word in ['fetch', 'download', 'scrape']):
            return 'data_retrieval'
        else:
            return 'general'
    
    def record_usage(self, task: str, tokens_used: int):
        """Record actual token usage for learning."""
        task_type = self._classify_task(task)
        
        if task_type not in self.usage_patterns:
            # Create new pattern
            self.usage_patterns[task_type] = TokenUsagePattern(
                task_type=task_type,
                avg_tokens=float(tokens_used),
                std_deviation=0.0,
                sample_count=1,
                last_updated=datetime.now()
            )
        else:
            # Update existing pattern using incremental statistics
            pattern = self.usage_patterns[task_type]
            
            # Update average and standard deviation incrementally
            n = pattern.sample_count
            old_avg = pattern.avg_tokens
            new_avg = (old_avg * n + tokens_used) / (n + 1)
            
            # Update standard deviation
            if n > 1:
                old_var = pattern.std_deviation ** 2
                new_var = ((n - 1) * old_var + n * (old_avg - new_avg) ** 2 + 
                          (tokens_used - new_avg) ** 2) / n
                pattern.std_deviation = np.sqrt(new_var)
            else:
                pattern.std_deviation = abs(tokens_used - new_avg)
            
            pattern.avg_tokens = new_avg
            pattern.sample_count += 1
            pattern.last_updated = datetime.now()
        
        # Save patterns periodically
        if sum(p.sample_count for p in self.usage_patterns.values()) % 10 == 0:
            self._save_patterns()
    
    def prioritize_context(self, history: List[Any], current_task: str) -> List[Any]:
        """
        Prioritize context items based on relevance to current task.
        
        Returns:
            Reordered history with most relevant items first
        """
        if len(history) <= 2:
            return history  # Too small to prioritize
        
        # Calculate priorities for each item
        priorities = []
        
        for i, item in enumerate(history):
            content_str = str(item)
            content_hash = str(hash(content_str))
            
            # Calculate relevance to current task
            relevance = self._calculate_relevance(content_str, current_task)
            
            # Calculate recency (newer items get higher scores)
            recency = (i + 1) / len(history)
            
            # Check if referenced recently
            reference_count = self.context_priorities.get(
                content_hash, 
                ContextPriority(content_hash, 0, 0, 0, datetime.now())
            ).reference_count
            
            priority = ContextPriority(
                content_hash=content_hash,
                relevance_score=relevance,
                recency_score=recency,
                reference_count=reference_count,
                timestamp=datetime.now()
            )
            
            priorities.append((priority, item))
            self.context_priorities[content_hash] = priority
        
        # Sort by priority score
        priorities.sort(key=lambda x: x[0].priority_score, reverse=True)
        
        # Return reordered items
        return [item for _, item in priorities]
    
    def _calculate_relevance(self, content: str, task: str) -> float:
        """Calculate relevance score between content and task."""
        # Simple keyword-based relevance
        task_words = set(task.lower().split())
        content_words = set(content.lower().split())
        
        if not task_words:
            return 0.0
        
        # Jaccard similarity
        intersection = len(task_words & content_words)
        union = len(task_words | content_words)
        
        return intersection / union if union > 0 else 0.0
    
    def get_token_budget(self, task: str) -> Dict[str, int]:
        """
        Get recommended token budget allocation for a task.
        
        Returns:
            Dictionary with token allocations for different components
        """
        total_budget = self.max_context_tokens - self.safety_margin
        predicted_usage, confidence = self.predict_token_usage(task)
        
        # Allocate tokens based on prediction
        allocations = {
            'system_prompt': 1000,  # Fixed for system instructions
            'conversation_history': min(total_budget * 0.6, total_budget - predicted_usage - 2000),
            'current_task': predicted_usage + confidence,
            'response_buffer': max(5000, total_budget * 0.2),
            'safety_margin': self.safety_margin
        }
        
        # Ensure we don't exceed total budget
        total_allocated = sum(allocations.values())
        if total_allocated > total_budget:
            # Scale down proportionally
            scale_factor = total_budget / total_allocated
            for key in allocations:
                allocations[key] = int(allocations[key] * scale_factor)
        
        return allocations
    
    def optimize_context_window(self, history: List[Any], current_task: str,
                                system_prompt: str = "") -> Tuple[List[Any], Dict[str, Any]]:
        """
        Optimize context window for maximum effectiveness.
        
        Returns:
            Tuple of (optimized_history, optimization_stats)
        """
        # Get token budget
        budget = self.get_token_budget(current_task)
        
        # Prioritize context
        prioritized_history = self.prioritize_context(history, current_task)
        
        # Trim to fit budget
        optimized_history = []
        current_tokens = self.count_tokens(system_prompt) + self.count_tokens(current_task)
        
        for item in prioritized_history:
            item_tokens = self.count_tokens(str(item))
            if current_tokens + item_tokens < budget['conversation_history']:
                optimized_history.append(item)
                current_tokens += item_tokens
            else:
                break
        
        # Calculate optimization statistics
        stats = {
            'original_items': len(history),
            'optimized_items': len(optimized_history),
            'tokens_used': current_tokens,
            'tokens_saved': self.count_tokens(str(history)) - current_tokens,
            'utilization': current_tokens / self.max_context_tokens
        }
        
        return optimized_history, stats
    
    def suggest_context_management(self) -> List[str]:
        """Provide suggestions for better context management."""
        suggestions = []
        
        # Analyze usage patterns
        if self.usage_patterns:
            high_usage_tasks = [
                pattern for pattern in self.usage_patterns.values()
                if pattern.avg_tokens > self.max_context_tokens * 0.5
            ]
            
            if high_usage_tasks:
                suggestions.append(
                    f"Consider breaking down {high_usage_tasks[0].task_type} tasks "
                    f"(avg {int(high_usage_tasks[0].avg_tokens)} tokens)"
                )
        
        # Check context priorities
        low_relevance_items = [
            cp for cp in self.context_priorities.values()
            if cp.relevance_score < 0.1 and cp.reference_count < 2
        ]
        
        if len(low_relevance_items) > 5:
            suggestions.append(
                "Consider clearing conversation history - many items have low relevance"
            )
        
        # Check token utilization
        recent_tasks = list(self.task_history)[-10:]
        if recent_tasks:
            avg_utilization = np.mean([
                self.count_tokens(task) / self.max_context_tokens 
                for task in recent_tasks
            ])
            
            if avg_utilization > 0.8:
                suggestions.append(
                    "Running close to token limits - consider more concise prompts"
                )
        
        return suggestions