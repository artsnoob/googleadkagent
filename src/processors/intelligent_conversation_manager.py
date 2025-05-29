"""
Intelligent conversation management with pattern recognition and optimization suggestions.
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import re
import json
from pathlib import Path
from enum import Enum

from .conversation_logger import ConversationLogger


class ConversationPhase(Enum):
    """Phases of a conversation."""
    GREETING = "greeting"
    EXPLORATION = "exploration"
    TASK_EXECUTION = "task_execution"
    CLARIFICATION = "clarification"
    COMPLETION = "completion"
    ERROR_RECOVERY = "error_recovery"


class TaskCategory(Enum):
    """Categories of tasks in conversations."""
    INFORMATION_RETRIEVAL = "information_retrieval"
    CONTENT_CREATION = "content_creation"
    DATA_ANALYSIS = "data_analysis"
    FILE_MANAGEMENT = "file_management"
    AUTOMATION = "automation"
    TROUBLESHOOTING = "troubleshooting"
    GENERAL = "general"


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation."""
    timestamp: datetime
    user_message: str
    assistant_response: str
    tools_used: List[str] = field(default_factory=list)
    tokens_used: int = 0
    success: bool = True
    phase: ConversationPhase = ConversationPhase.TASK_EXECUTION
    category: TaskCategory = TaskCategory.GENERAL


@dataclass
class ConversationPattern:
    """Represents a detected pattern in conversations."""
    pattern_type: str
    description: str
    occurrences: int
    last_seen: datetime
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ConversationMetrics:
    """Metrics about the conversation."""
    total_turns: int = 0
    successful_turns: int = 0
    failed_turns: int = 0
    total_tokens: int = 0
    tools_usage: Dict[str, int] = field(default_factory=dict)
    phase_distribution: Dict[ConversationPhase, int] = field(default_factory=dict)
    category_distribution: Dict[TaskCategory, int] = field(default_factory=dict)
    avg_response_time: float = 0.0
    user_satisfaction_indicators: Dict[str, int] = field(default_factory=dict)


class IntelligentConversationManager:
    """Manages conversations with intelligence and pattern recognition."""
    
    def __init__(self, conversation_logger: ConversationLogger, 
                 patterns_file: Optional[Path] = None):
        self.logger = conversation_logger
        self.current_conversation: List[ConversationTurn] = []
        self.all_conversations: List[List[ConversationTurn]] = []
        self.detected_patterns: Dict[str, ConversationPattern] = {}
        self.patterns_file = patterns_file or Path("./agent_files/conversation_patterns.json")
        self.current_phase = ConversationPhase.GREETING
        self._load_patterns()
    
    def _load_patterns(self):
        """Load learned conversation patterns."""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    data = json.load(f)
                    for pattern_data in data.get('patterns', []):
                        pattern = ConversationPattern(
                            pattern_type=pattern_data['pattern_type'],
                            description=pattern_data['description'],
                            occurrences=pattern_data['occurrences'],
                            last_seen=datetime.fromisoformat(pattern_data['last_seen']),
                            suggestions=pattern_data.get('suggestions', [])
                        )
                        self.detected_patterns[pattern.pattern_type] = pattern
            except Exception:
                pass
    
    def _save_patterns(self):
        """Save detected patterns for future use."""
        try:
            self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
            patterns_data = []
            
            for pattern in self.detected_patterns.values():
                patterns_data.append({
                    'pattern_type': pattern.pattern_type,
                    'description': pattern.description,
                    'occurrences': pattern.occurrences,
                    'last_seen': pattern.last_seen.isoformat(),
                    'suggestions': pattern.suggestions
                })
            
            with open(self.patterns_file, 'w') as f:
                json.dump({'patterns': patterns_data}, f, indent=2)
        except Exception:
            pass
    
    def add_turn(self, user_message: str, assistant_response: str, 
                 tools_used: List[str] = None, tokens_used: int = 0, 
                 success: bool = True):
        """Add a conversation turn and analyze it."""
        # Determine phase and category
        phase = self._determine_phase(user_message, assistant_response)
        category = self._categorize_task(user_message)
        
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_message=user_message,
            assistant_response=assistant_response,
            tools_used=tools_used or [],
            tokens_used=tokens_used,
            success=success,
            phase=phase,
            category=category
        )
        
        self.current_conversation.append(turn)
        self.current_phase = phase
        
        # Analyze for patterns
        self._analyze_patterns()
    
    def _determine_phase(self, user_message: str, assistant_response: str) -> ConversationPhase:
        """Determine the current phase of conversation."""
        user_lower = user_message.lower()
        assistant_lower = assistant_response.lower()
        
        # Greeting detection
        greeting_patterns = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        if any(pattern in user_lower for pattern in greeting_patterns):
            return ConversationPhase.GREETING
        
        # Error recovery detection
        error_indicators = ['error', 'failed', 'problem', "doesn't work", "not working"]
        if any(indicator in assistant_lower for indicator in error_indicators):
            return ConversationPhase.ERROR_RECOVERY
        
        # Clarification detection
        clarification_indicators = ['?', 'what do you mean', 'can you explain', 'which']
        if any(indicator in user_lower for indicator in clarification_indicators):
            return ConversationPhase.CLARIFICATION
        
        # Completion detection
        completion_indicators = ['done', 'completed', 'finished', 'thank you', 'thanks']
        if any(indicator in user_lower for indicator in completion_indicators):
            return ConversationPhase.COMPLETION
        
        # Exploration vs execution
        exploration_keywords = ['how', 'what', 'when', 'where', 'why', 'can you']
        if any(keyword in user_lower for keyword in exploration_keywords):
            return ConversationPhase.EXPLORATION
        
        return ConversationPhase.TASK_EXECUTION
    
    def _categorize_task(self, user_message: str) -> TaskCategory:
        """Categorize the type of task being requested."""
        message_lower = user_message.lower()
        
        # Category keywords mapping
        category_keywords = {
            TaskCategory.INFORMATION_RETRIEVAL: ['search', 'find', 'what is', 'tell me about', 'research'],
            TaskCategory.CONTENT_CREATION: ['create', 'write', 'generate', 'make', 'build'],
            TaskCategory.DATA_ANALYSIS: ['analyze', 'calculate', 'process', 'visualize', 'chart'],
            TaskCategory.FILE_MANAGEMENT: ['file', 'folder', 'directory', 'save', 'load', 'delete'],
            TaskCategory.AUTOMATION: ['automate', 'schedule', 'script', 'run', 'execute'],
            TaskCategory.TROUBLESHOOTING: ['fix', 'debug', 'error', 'problem', 'issue']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        
        return TaskCategory.GENERAL
    
    def _analyze_patterns(self):
        """Analyze conversation for patterns."""
        if len(self.current_conversation) < 2:
            return
        
        # Pattern: Repeated similar requests
        self._detect_repetition_pattern()
        
        # Pattern: Task sequences
        self._detect_task_sequences()
        
        # Pattern: Error patterns
        self._detect_error_patterns()
        
        # Pattern: Inefficient workflows
        self._detect_inefficient_workflows()
        
        # Save patterns periodically
        if len(self.current_conversation) % 10 == 0:
            self._save_patterns()
    
    def _detect_repetition_pattern(self):
        """Detect when users repeat similar requests."""
        if len(self.current_conversation) < 3:
            return
        
        # Check last 5 turns for similar requests
        recent_turns = self.current_conversation[-5:]
        messages = [turn.user_message.lower() for turn in recent_turns]
        
        # Simple similarity check (can be made more sophisticated)
        message_counter = Counter(messages)
        for message, count in message_counter.items():
            if count >= 2:
                pattern_key = f"repetition_{hash(message) % 1000}"
                
                if pattern_key not in self.detected_patterns:
                    self.detected_patterns[pattern_key] = ConversationPattern(
                        pattern_type="repetition",
                        description=f"User repeatedly asks similar questions",
                        occurrences=1,
                        last_seen=datetime.now(),
                        suggestions=[
                            "Consider creating a saved response or automation for this common request",
                            "The user might need clearer initial responses"
                        ]
                    )
                else:
                    pattern = self.detected_patterns[pattern_key]
                    pattern.occurrences += 1
                    pattern.last_seen = datetime.now()
    
    def _detect_task_sequences(self):
        """Detect common task sequences that could be automated."""
        if len(self.current_conversation) < 3:
            return
        
        # Look for sequences of tasks
        recent_categories = [turn.category for turn in self.current_conversation[-5:]]
        
        # Common sequences
        common_sequences = [
            ([TaskCategory.INFORMATION_RETRIEVAL, TaskCategory.CONTENT_CREATION], 
             "research_then_create"),
            ([TaskCategory.FILE_MANAGEMENT, TaskCategory.DATA_ANALYSIS], 
             "load_then_analyze"),
            ([TaskCategory.DATA_ANALYSIS, TaskCategory.CONTENT_CREATION], 
             "analyze_then_report")
        ]
        
        for sequence, pattern_name in common_sequences:
            if self._contains_sequence(recent_categories, sequence):
                if pattern_name not in self.detected_patterns:
                    self.detected_patterns[pattern_name] = ConversationPattern(
                        pattern_type="task_sequence",
                        description=f"Common sequence: {' → '.join(cat.value for cat in sequence)}",
                        occurrences=1,
                        last_seen=datetime.now(),
                        suggestions=[
                            f"Consider creating a workflow that combines these steps",
                            f"This sequence appears frequently and could be automated"
                        ]
                    )
                else:
                    pattern = self.detected_patterns[pattern_name]
                    pattern.occurrences += 1
                    pattern.last_seen = datetime.now()
    
    def _contains_sequence(self, categories: List[TaskCategory], 
                           sequence: List[TaskCategory]) -> bool:
        """Check if a sequence exists in the categories list."""
        for i in range(len(categories) - len(sequence) + 1):
            if categories[i:i+len(sequence)] == sequence:
                return True
        return False
    
    def _detect_error_patterns(self):
        """Detect recurring error patterns."""
        error_turns = [turn for turn in self.current_conversation 
                      if not turn.success or turn.phase == ConversationPhase.ERROR_RECOVERY]
        
        if len(error_turns) >= 2:
            # Group by tools that cause errors
            tool_errors = defaultdict(int)
            for turn in error_turns:
                for tool in turn.tools_used:
                    tool_errors[tool] += 1
            
            for tool, count in tool_errors.items():
                if count >= 2:
                    pattern_key = f"tool_errors_{tool}"
                    if pattern_key not in self.detected_patterns:
                        self.detected_patterns[pattern_key] = ConversationPattern(
                            pattern_type="error_pattern",
                            description=f"Frequent errors with {tool}",
                            occurrences=count,
                            last_seen=datetime.now(),
                            suggestions=[
                                f"Consider using alternative to {tool}",
                                f"Check {tool} configuration or availability",
                                f"Implement better error handling for {tool}"
                            ]
                        )
    
    def _detect_inefficient_workflows(self):
        """Detect workflows that could be optimized."""
        # High token usage for simple tasks
        high_token_turns = [turn for turn in self.current_conversation[-10:]
                           if turn.tokens_used > 5000 and 
                           turn.category in [TaskCategory.GENERAL, TaskCategory.FILE_MANAGEMENT]]
        
        if len(high_token_turns) >= 2:
            if "high_token_usage" not in self.detected_patterns:
                self.detected_patterns["high_token_usage"] = ConversationPattern(
                    pattern_type="inefficiency",
                    description="High token usage for simple tasks",
                    occurrences=len(high_token_turns),
                    last_seen=datetime.now(),
                    suggestions=[
                        "Consider more direct approaches for simple tasks",
                        "Reduce conversation context for basic operations",
                        "Use specialized agents instead of general agent"
                    ]
                )
    
    def get_conversation_metrics(self) -> ConversationMetrics:
        """Get comprehensive metrics about the current conversation."""
        metrics = ConversationMetrics()
        
        if not self.current_conversation:
            return metrics
        
        metrics.total_turns = len(self.current_conversation)
        metrics.successful_turns = sum(1 for turn in self.current_conversation if turn.success)
        metrics.failed_turns = metrics.total_turns - metrics.successful_turns
        metrics.total_tokens = sum(turn.tokens_used for turn in self.current_conversation)
        
        # Tool usage statistics
        for turn in self.current_conversation:
            for tool in turn.tools_used:
                metrics.tools_usage[tool] = metrics.tools_usage.get(tool, 0) + 1
        
        # Phase and category distribution
        for turn in self.current_conversation:
            metrics.phase_distribution[turn.phase] = metrics.phase_distribution.get(turn.phase, 0) + 1
            metrics.category_distribution[turn.category] = metrics.category_distribution.get(turn.category, 0) + 1
        
        # User satisfaction indicators
        for turn in self.current_conversation:
            user_lower = turn.user_message.lower()
            if any(word in user_lower for word in ['thank', 'great', 'perfect', 'excellent']):
                metrics.user_satisfaction_indicators['positive'] = metrics.user_satisfaction_indicators.get('positive', 0) + 1
            elif any(word in user_lower for word in ['frustrated', 'annoying', 'slow', 'confused']):
                metrics.user_satisfaction_indicators['negative'] = metrics.user_satisfaction_indicators.get('negative', 0) + 1
        
        return metrics
    
    def suggest_conversation_improvements(self) -> List[str]:
        """Provide suggestions for improving the conversation flow."""
        suggestions = []
        metrics = self.get_conversation_metrics()
        
        # Based on metrics
        if metrics.failed_turns > metrics.total_turns * 0.3:
            suggestions.append("High failure rate detected. Consider reviewing error patterns and tool configurations.")
        
        if metrics.total_tokens > metrics.total_turns * 2000:
            suggestions.append("High token usage per turn. Consider more concise interactions.")
        
        # Based on patterns
        for pattern in self.detected_patterns.values():
            if pattern.occurrences >= 3 and (datetime.now() - pattern.last_seen) < timedelta(hours=1):
                suggestions.extend(pattern.suggestions)
        
        # Phase-based suggestions
        if ConversationPhase.CLARIFICATION in metrics.phase_distribution:
            clarification_rate = metrics.phase_distribution[ConversationPhase.CLARIFICATION] / metrics.total_turns
            if clarification_rate > 0.3:
                suggestions.append("High clarification rate. Consider providing more detailed initial responses.")
        
        # Tool optimization
        if len(metrics.tools_usage) > 5:
            suggestions.append("Many different tools used. Consider if all are necessary for the task.")
        
        return list(set(suggestions))  # Remove duplicates
    
    def get_workflow_recommendation(self) -> Optional[Dict[str, Any]]:
        """Recommend a workflow based on detected patterns."""
        # Find most common task sequences
        sequence_patterns = [p for p in self.detected_patterns.values() 
                            if p.pattern_type == "task_sequence" and p.occurrences >= 3]
        
        if not sequence_patterns:
            return None
        
        # Get the most frequent sequence
        most_frequent = max(sequence_patterns, key=lambda p: p.occurrences)
        
        # Parse the sequence from description
        sequence_match = re.search(r"Common sequence: (.+)", most_frequent.description)
        if sequence_match:
            steps = sequence_match.group(1).split(' → ')
            
            return {
                "name": f"Automated {most_frequent.description}",
                "steps": steps,
                "frequency": most_frequent.occurrences,
                "estimated_time_savings": f"{most_frequent.occurrences * 2} minutes per week",
                "implementation": "Create a composite agent or workflow automation"
            }
        
        return None
    
    def end_conversation(self):
        """Mark the end of current conversation and analyze overall patterns."""
        if self.current_conversation:
            self.all_conversations.append(self.current_conversation)
            
            # Final analysis
            metrics = self.get_conversation_metrics()
            improvements = self.suggest_conversation_improvements()
            
            # Log insights
            if self.logger:
                self.logger.add_metadata({
                    "conversation_metrics": {
                        "total_turns": metrics.total_turns,
                        "success_rate": metrics.successful_turns / metrics.total_turns if metrics.total_turns > 0 else 0,
                        "total_tokens": metrics.total_tokens,
                        "primary_category": max(metrics.category_distribution.items(), key=lambda x: x[1])[0].value if metrics.category_distribution else "none"
                    },
                    "improvements": improvements
                })
            
            # Reset for next conversation
            self.current_conversation = []
            self.current_phase = ConversationPhase.GREETING