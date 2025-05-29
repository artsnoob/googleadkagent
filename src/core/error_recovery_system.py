"""
Advanced Error Recovery System for Google ADK Agent

This module implements a comprehensive multi-layered fallback system that enables
the agent to gracefully handle various types of failures and provide alternative
solutions when primary tools or approaches fail.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class FailureType(Enum):
    """Categories of failures the system can handle"""
    TOOL_UNAVAILABLE = "tool_unavailable"
    TOOL_EXECUTION_ERROR = "tool_execution_error"
    NETWORK_ERROR = "network_error"
    API_RATE_LIMIT = "api_rate_limit"
    PERMISSION_ERROR = "permission_error"
    TIMEOUT_ERROR = "timeout_error"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    INVALID_INPUT = "invalid_input"
    SERVICE_UNAVAILABLE = "service_unavailable"

class FallbackStrategy(Enum):
    """Available fallback strategies"""
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    USE_ALTERNATIVE_TOOL = "use_alternative_tool"
    DEGRADE_GRACEFULLY = "degrade_gracefully"
    CUSTOM_SCRIPT_GENERATION = "custom_script_generation"
    HUMAN_READABLE_ERROR = "human_readable_error"
    CROSS_AGENT_COORDINATION = "cross_agent_coordination"

@dataclass
class FailureContext:
    """Context information about a failure"""
    failure_type: FailureType
    error_message: str
    tool_name: Optional[str] = None
    agent_name: Optional[str] = None
    user_intent: Optional[str] = None
    retry_count: int = 0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class FallbackResult:
    """Result of applying a fallback strategy"""
    success: bool
    strategy_used: FallbackStrategy
    alternative_action: Optional[str] = None
    user_message: Optional[str] = None
    retry_suggested: bool = False
    learning_note: Optional[str] = None

class ErrorRecoverySystem:
    """
    Comprehensive error recovery system with multiple fallback strategies
    """
    
    def __init__(self):
        self.failure_history: List[FailureContext] = []
        self.strategy_effectiveness: Dict[str, float] = {}
        self.retry_limits = {
            FailureType.NETWORK_ERROR: 3,
            FailureType.API_RATE_LIMIT: 2,
            FailureType.TIMEOUT_ERROR: 2,
            FailureType.SERVICE_UNAVAILABLE: 3,
            FailureType.TOOL_EXECUTION_ERROR: 1,
        }
        
        # Tool alternatives mapping
        self.tool_alternatives = {
            'filesystem_agent': ['mcp_code_executor_agent'],  # Use code to handle files
            'search_agent': ['perplexity_agent', 'fetch_agent'],  # Alternative research
            'content_scraper_agent': ['fetch_agent', 'search_agent'],  # Alternative content gathering
            'fetch_agent': ['mcp_code_executor_agent'],  # Use requests library via code
            'perplexity_agent': ['search_agent'],  # Use Google search as fallback
            'mcp_code_executor_agent': []  # No direct alternative, but can suggest manual execution
        }
        
        # Common error patterns and their solutions
        self.error_patterns = {
            'permission denied': FailureType.PERMISSION_ERROR,
            'connection refused': FailureType.NETWORK_ERROR,
            'timeout': FailureType.TIMEOUT_ERROR,
            'rate limit': FailureType.API_RATE_LIMIT,
            'not found': FailureType.TOOL_UNAVAILABLE,
            'service unavailable': FailureType.SERVICE_UNAVAILABLE,
            'invalid argument': FailureType.INVALID_INPUT,
        }
    
    def classify_failure(self, error_message: str, tool_name: str = None) -> FailureType:
        """Classify the type of failure based on error message"""
        error_lower = error_message.lower()
        
        for pattern, failure_type in self.error_patterns.items():
            if pattern in error_lower:
                return failure_type
        
        # Default classification
        if tool_name and 'mcp' in tool_name.lower():
            return FailureType.SERVICE_UNAVAILABLE
        
        return FailureType.TOOL_EXECUTION_ERROR
    
    async def handle_failure(self, context: FailureContext) -> FallbackResult:
        """
        Main entry point for handling failures with appropriate fallback strategies
        """
        # Record the failure
        self.failure_history.append(context)
        
        # Determine the best fallback strategy
        strategies = self._get_applicable_strategies(context)
        
        # Try strategies in order of effectiveness
        for strategy in strategies:
            try:
                result = await self._apply_strategy(strategy, context)
                if result.success:
                    self._record_success(strategy, context)
                    return result
            except Exception as e:
                # Strategy itself failed, try next one
                continue
        
        # All strategies failed, return graceful degradation
        return FallbackResult(
            success=False,
            strategy_used=FallbackStrategy.HUMAN_READABLE_ERROR,
            user_message=self._generate_helpful_error_message(context),
            learning_note=f"All strategies failed for {context.failure_type}"
        )
    
    def _get_applicable_strategies(self, context: FailureContext) -> List[FallbackStrategy]:
        """Determine which fallback strategies apply to this failure type"""
        strategies = []
        
        # Retry-based strategies for transient failures
        if context.failure_type in [FailureType.NETWORK_ERROR, FailureType.API_RATE_LIMIT, 
                                   FailureType.TIMEOUT_ERROR, FailureType.SERVICE_UNAVAILABLE]:
            if context.retry_count < self.retry_limits.get(context.failure_type, 1):
                strategies.append(FallbackStrategy.RETRY_WITH_BACKOFF)
        
        # Tool alternatives
        if context.failure_type in [FailureType.TOOL_UNAVAILABLE, FailureType.TOOL_EXECUTION_ERROR]:
            if context.tool_name and context.tool_name in self.tool_alternatives:
                strategies.append(FallbackStrategy.USE_ALTERNATIVE_TOOL)
            strategies.append(FallbackStrategy.CUSTOM_SCRIPT_GENERATION)
            strategies.append(FallbackStrategy.CROSS_AGENT_COORDINATION)
        
        # Permission and input errors
        if context.failure_type in [FailureType.PERMISSION_ERROR, FailureType.INVALID_INPUT]:
            strategies.append(FallbackStrategy.DEGRADE_GRACEFULLY)
        
        # Always include graceful degradation as last resort
        strategies.append(FallbackStrategy.HUMAN_READABLE_ERROR)
        
        return strategies
    
    async def _apply_strategy(self, strategy: FallbackStrategy, context: FailureContext) -> FallbackResult:
        """Apply a specific fallback strategy"""
        
        if strategy == FallbackStrategy.RETRY_WITH_BACKOFF:
            return await self._retry_with_backoff(context)
        
        elif strategy == FallbackStrategy.USE_ALTERNATIVE_TOOL:
            return self._use_alternative_tool(context)
        
        elif strategy == FallbackStrategy.CUSTOM_SCRIPT_GENERATION:
            return self._suggest_custom_script(context)
        
        elif strategy == FallbackStrategy.CROSS_AGENT_COORDINATION:
            return self._suggest_cross_agent_solution(context)
        
        elif strategy == FallbackStrategy.DEGRADE_GRACEFULLY:
            return self._degrade_gracefully(context)
        
        elif strategy == FallbackStrategy.HUMAN_READABLE_ERROR:
            return FallbackResult(
                success=True,  # Success in providing helpful error
                strategy_used=strategy,
                user_message=self._generate_helpful_error_message(context)
            )
        
        return FallbackResult(success=False, strategy_used=strategy)
    
    async def _retry_with_backoff(self, context: FailureContext) -> FallbackResult:
        """Implement exponential backoff retry strategy"""
        wait_time = min(2 ** context.retry_count, 30)  # Cap at 30 seconds
        
        return FallbackResult(
            success=True,
            strategy_used=FallbackStrategy.RETRY_WITH_BACKOFF,
            alternative_action=f"retry_after_{wait_time}_seconds",
            user_message=f"Retrying in {wait_time} seconds due to {context.failure_type.value}...",
            retry_suggested=True
        )
    
    def _use_alternative_tool(self, context: FailureContext) -> FallbackResult:
        """Suggest using an alternative tool"""
        alternatives = self.tool_alternatives.get(context.tool_name, [])
        
        if not alternatives:
            return FallbackResult(success=False, strategy_used=FallbackStrategy.USE_ALTERNATIVE_TOOL)
        
        best_alternative = alternatives[0]  # Could be more sophisticated
        
        return FallbackResult(
            success=True,
            strategy_used=FallbackStrategy.USE_ALTERNATIVE_TOOL,
            alternative_action=f"use_{best_alternative}",
            user_message=f"The {context.tool_name} is unavailable. I'll use {best_alternative} instead.",
            learning_note=f"Fallback from {context.tool_name} to {best_alternative}"
        )
    
    def _suggest_custom_script(self, context: FailureContext) -> FallbackResult:
        """Suggest generating a custom script to solve the problem"""
        script_suggestions = {
            'filesystem_agent': "I'll write a Python script using os and shutil libraries to handle file operations.",
            'fetch_agent': "I'll write a Python script using requests library to fetch web content.",
            'content_scraper_agent': "I'll write a Python script using beautifulsoup4 and requests to scrape content.",
            'search_agent': "I'll write a Python script using web scraping to gather information.",
        }
        
        suggestion = script_suggestions.get(context.tool_name, 
            "I'll write a custom Python script to accomplish this task.")
        
        return FallbackResult(
            success=True,
            strategy_used=FallbackStrategy.CUSTOM_SCRIPT_GENERATION,
            alternative_action="generate_custom_script",
            user_message=suggestion,
            learning_note=f"Custom script generated for {context.tool_name} failure"
        )
    
    def _suggest_cross_agent_solution(self, context: FailureContext) -> FallbackResult:
        """Suggest using multiple agents in coordination"""
        coordination_patterns = {
            'filesystem_agent': "I'll use the code executor to handle file operations and search agent to find relevant information.",
            'search_agent': "I'll combine the fetch agent and perplexity agent to gather comprehensive information.",
            'content_scraper_agent': "I'll use the fetch agent to get content and code executor to process it.",
        }
        
        suggestion = coordination_patterns.get(context.tool_name,
            "I'll coordinate multiple agents to accomplish this task.")
        
        return FallbackResult(
            success=True,
            strategy_used=FallbackStrategy.CROSS_AGENT_COORDINATION,
            alternative_action="coordinate_multiple_agents",
            user_message=suggestion,
            learning_note=f"Multi-agent coordination for {context.tool_name}"
        )
    
    def _degrade_gracefully(self, context: FailureContext) -> FallbackResult:
        """Provide a graceful degradation of functionality"""
        degradation_messages = {
            FailureType.PERMISSION_ERROR: "I don't have the necessary permissions. I'll provide instructions for you to complete this manually.",
            FailureType.INVALID_INPUT: "The input format isn't quite right. Let me suggest the correct format and try again.",
            FailureType.RESOURCE_EXHAUSTED: "System resources are currently limited. I'll provide a simplified approach.",
        }
        
        message = degradation_messages.get(context.failure_type,
            "I'll provide an alternative approach to accomplish your goal.")
        
        return FallbackResult(
            success=True,
            strategy_used=FallbackStrategy.DEGRADE_GRACEFULLY,
            user_message=message,
            learning_note=f"Graceful degradation for {context.failure_type}"
        )
    
    def _generate_helpful_error_message(self, context: FailureContext) -> str:
        """Generate a helpful, human-readable error message with suggestions"""
        
        # Map failure types to symbols and colors for better visualization
        error_symbols = {
            FailureType.TOOL_UNAVAILABLE: (SYMBOL_WARNING, COLOR_WARNING),
            FailureType.NETWORK_ERROR: (SYMBOL_RETRY, COLOR_INFO),
            FailureType.API_RATE_LIMIT: (SYMBOL_WARNING, COLOR_WARNING),
            FailureType.PERMISSION_ERROR: (SYMBOL_ERROR, COLOR_ERROR),
            FailureType.TIMEOUT_ERROR: (SYMBOL_WARNING, COLOR_WARNING),
            FailureType.INVALID_INPUT: (SYMBOL_MANUAL, COLOR_INFO),
            FailureType.SERVICE_UNAVAILABLE: (SYMBOL_WARNING, COLOR_WARNING),
        }
        
        symbol, color = error_symbols.get(context.failure_type, (SYMBOL_ERROR, COLOR_ERROR))
        
        suggestions = {
            FailureType.TOOL_UNAVAILABLE: "This tool isn't available right now. Let me try a different approach.",
            FailureType.NETWORK_ERROR: "There's a network connectivity issue. This is usually temporary.",
            FailureType.API_RATE_LIMIT: "I've hit a rate limit. I'll wait a moment before trying again.",
            FailureType.PERMISSION_ERROR: "I don't have the necessary permissions for this operation.",
            FailureType.TIMEOUT_ERROR: "The operation timed out. Let me try with a simpler approach.",
            FailureType.INVALID_INPUT: "The input format needs adjustment. Let me help you with the correct format.",
        }
        
        suggestion = suggestions.get(context.failure_type, "Let me try a different approach.")
        
        return f"{color}{symbol} {context.error_message}{COLOR_RESET}\n{COLOR_INFO}→ {suggestion}{COLOR_RESET}"
    
    def _record_success(self, strategy: FallbackStrategy, context: FailureContext):
        """Record successful strategy application for learning"""
        key = f"{context.failure_type}_{strategy}"
        current_rate = self.strategy_effectiveness.get(key, 0.5)
        # Simple learning: increase success rate
        self.strategy_effectiveness[key] = min(current_rate + 0.1, 1.0)
    
    def get_failure_stats(self) -> Dict[str, Any]:
        """Get statistics about failures and recovery effectiveness"""
        if not self.failure_history:
            return {"total_failures": 0}
        
        failure_counts = {}
        for failure in self.failure_history:
            failure_counts[failure.failure_type] = failure_counts.get(failure.failure_type, 0) + 1
        
        recent_failures = [f for f in self.failure_history 
                          if f.timestamp > datetime.now() - timedelta(hours=1)]
        
        return {
            "total_failures": len(self.failure_history),
            "recent_failures": len(recent_failures),
            "failure_types": failure_counts,
            "strategy_effectiveness": self.strategy_effectiveness,
            "most_common_failure": max(failure_counts.items(), key=lambda x: x[1])[0] if failure_counts else None
        }


# Utility functions for integration with the main agent

def create_failure_context(error: Exception, tool_name: str = None, agent_name: str = None, 
                          user_intent: str = None, retry_count: int = 0) -> FailureContext:
    """Helper function to create a FailureContext from an exception"""
    error_recovery = ErrorRecoverySystem()
    failure_type = error_recovery.classify_failure(str(error), tool_name)
    
    return FailureContext(
        failure_type=failure_type,
        error_message=str(error),
        tool_name=tool_name,
        agent_name=agent_name,
        user_intent=user_intent,
        retry_count=retry_count
    )

async def handle_tool_failure(error: Exception, tool_name: str, user_intent: str = None) -> FallbackResult:
    """Convenient function to handle tool failures"""
    error_recovery = ErrorRecoverySystem()
    context = create_failure_context(error, tool_name=tool_name, user_intent=user_intent)
    return await error_recovery.handle_failure(context)

# Color constants for consistent output formatting
COLOR_ERROR = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_SUCCESS = "\033[92m"
COLOR_INFO = "\033[94m"
COLOR_RESET = "\033[0m"

# Error visualization symbols
SYMBOL_ERROR = "✗"
SYMBOL_WARNING = "⚠"
SYMBOL_RETRY = "🔁"
SYMBOL_FALLBACK = "🔄"
SYMBOL_MANUAL = "👤"