"""
Enhanced Error Recovery System with Circuit Breaker and Learning Capabilities
"""
import asyncio
from typing import Dict, List, Optional, Callable, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path
from contextlib import asynccontextmanager

from .error_recovery_system import (
    ErrorRecoverySystem, FailureContext, FallbackResult,
    FailureType, FallbackStrategy
)


@dataclass
class CircuitState:
    """Represents the state of a circuit breaker."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class ServiceHealth:
    """Track health of a service/tool."""
    name: str
    failure_count: int = 0
    success_count: int = 0
    last_failure: Optional[datetime] = None
    last_success: Optional[datetime] = None
    circuit_state: str = CircuitState.CLOSED
    circuit_opened_at: Optional[datetime] = None
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        total = self.failure_count + self.success_count
        return self.failure_count / total if total > 0 else 0.0
    
    @property
    def should_open_circuit(self) -> bool:
        """Determine if circuit should open."""
        # Open circuit if failure rate > 50% with at least 5 attempts
        total = self.failure_count + self.success_count
        return total >= 5 and self.failure_rate > 0.5
    
    @property
    def should_test_circuit(self) -> bool:
        """Check if enough time passed to test circuit."""
        if self.circuit_opened_at:
            # Test after 30 seconds
            return datetime.now() - self.circuit_opened_at > timedelta(seconds=30)
        return False


class EnhancedErrorRecoverySystem(ErrorRecoverySystem):
    """Enhanced error recovery with circuit breaker and learning."""
    
    def __init__(self, learning_file: Optional[Path] = None):
        super().__init__()
        self.service_health: Dict[str, ServiceHealth] = {}
        self.learning_file = learning_file or Path("./agent_files/error_recovery_learning.json")
        self.recovery_patterns: Dict[str, List[Dict]] = {}
        self._load_learning_data()
    
    def _load_learning_data(self):
        """Load learned recovery patterns from file."""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r') as f:
                    data = json.load(f)
                    self.recovery_patterns = data.get('patterns', {})
                    self.strategy_effectiveness = data.get('effectiveness', {})
            except Exception:
                pass
    
    def _save_learning_data(self):
        """Save learned patterns for future use."""
        try:
            self.learning_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.learning_file, 'w') as f:
                json.dump({
                    'patterns': self.recovery_patterns,
                    'effectiveness': self.strategy_effectiveness
                }, f, indent=2, default=str)
        except Exception:
            pass
    
    @asynccontextmanager
    async def monitored_execution(self, service_name: str, operation_desc: str):
        """Context manager for monitored execution with circuit breaker."""
        # Check circuit breaker
        health = self.service_health.get(service_name, ServiceHealth(name=service_name))
        
        if health.circuit_state == CircuitState.OPEN:
            if health.should_test_circuit:
                health.circuit_state = CircuitState.HALF_OPEN
            else:
                raise Exception(f"Circuit breaker OPEN for {service_name}. Service temporarily unavailable.")
        
        try:
            # Execute operation
            yield
            
            # Record success
            health.success_count += 1
            health.last_success = datetime.now()
            
            # Close circuit if in half-open state
            if health.circuit_state == CircuitState.HALF_OPEN:
                health.circuit_state = CircuitState.CLOSED
                health.failure_count = 0  # Reset failure count
            
        except Exception as e:
            # Record failure
            health.failure_count += 1
            health.last_failure = datetime.now()
            
            # Check if circuit should open
            if health.should_open_circuit:
                health.circuit_state = CircuitState.OPEN
                health.circuit_opened_at = datetime.now()
            
            # Re-raise for handling
            raise
        
        finally:
            # Update service health
            self.service_health[service_name] = health
    
    async def handle_failure_with_learning(self, context: FailureContext) -> FallbackResult:
        """Enhanced failure handling with learning from past recoveries."""
        # Check if we've seen similar failures
        pattern_key = f"{context.failure_type}_{context.tool_name}"
        if pattern_key in self.recovery_patterns:
            # Use learned pattern
            for pattern in self.recovery_patterns[pattern_key]:
                if pattern['success_rate'] > 0.7:
                    # Apply successful pattern
                    result = await self._apply_learned_pattern(pattern, context)
                    if result.success:
                        return result
        
        # Fall back to standard handling
        result = await self.handle_failure(context)
        
        # Learn from the outcome
        self._record_recovery_pattern(context, result)
        
        return result
    
    async def _apply_learned_pattern(self, pattern: Dict, context: FailureContext) -> FallbackResult:
        """Apply a previously successful recovery pattern."""
        strategy = FallbackStrategy(pattern['strategy'])
        
        # Apply with learned parameters
        if strategy == FallbackStrategy.USE_ALTERNATIVE_TOOL:
            return FallbackResult(
                success=True,
                strategy_used=strategy,
                alternative_action=f"use_{pattern['alternative_tool']}",
                user_message=f"Using {pattern['alternative_tool']} (previously successful for this type of error)",
                learning_note=f"Applied learned pattern: {pattern['description']}"
            )
        
        # Default to standard strategy application
        return await self._apply_strategy(strategy, context)
    
    def _record_recovery_pattern(self, context: FailureContext, result: FallbackResult):
        """Record successful recovery patterns for learning."""
        if result.success:
            pattern_key = f"{context.failure_type}_{context.tool_name}"
            
            pattern = {
                'strategy': result.strategy_used.value,
                'timestamp': datetime.now().isoformat(),
                'description': result.learning_note or f"Recovered using {result.strategy_used.value}",
                'success_rate': 1.0
            }
            
            if result.alternative_action and 'use_' in result.alternative_action:
                pattern['alternative_tool'] = result.alternative_action.replace('use_', '')
            
            if pattern_key not in self.recovery_patterns:
                self.recovery_patterns[pattern_key] = []
            
            self.recovery_patterns[pattern_key].append(pattern)
            
            # Save learning data
            self._save_learning_data()
    
    def get_service_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report for all services."""
        report = {
            'healthy_services': [],
            'degraded_services': [],
            'unavailable_services': [],
            'circuit_breaker_status': {}
        }
        
        for name, health in self.service_health.items():
            status = {
                'name': name,
                'failure_rate': f"{health.failure_rate:.1%}",
                'circuit_state': health.circuit_state,
                'last_failure': health.last_failure.isoformat() if health.last_failure else None,
                'last_success': health.last_success.isoformat() if health.last_success else None
            }
            
            report['circuit_breaker_status'][name] = status
            
            if health.circuit_state == CircuitState.OPEN:
                report['unavailable_services'].append(name)
            elif health.failure_rate > 0.3:
                report['degraded_services'].append(name)
            else:
                report['healthy_services'].append(name)
        
        return report
    
    def suggest_preventive_measures(self) -> List[str]:
        """Suggest preventive measures based on failure patterns."""
        suggestions = []
        
        # Analyze failure patterns
        failure_counts = {}
        for failure in self.failure_history[-100:]:  # Last 100 failures
            key = (failure.failure_type, failure.tool_name)
            failure_counts[key] = failure_counts.get(key, 0) + 1
        
        # Generate suggestions
        for (failure_type, tool_name), count in failure_counts.items():
            if count > 5:
                if failure_type == FailureType.API_RATE_LIMIT:
                    suggestions.append(f"Consider implementing request caching for {tool_name}")
                elif failure_type == FailureType.TIMEOUT_ERROR:
                    suggestions.append(f"Increase timeout limits or batch operations for {tool_name}")
                elif failure_type == FailureType.NETWORK_ERROR:
                    suggestions.append(f"Implement offline mode or local caching for {tool_name}")
        
        return suggestions


class ErrorRecoveryMiddleware:
    """Middleware to automatically apply error recovery to agent operations."""
    
    def __init__(self, error_recovery: EnhancedErrorRecoverySystem):
        self.error_recovery = error_recovery
    
    async def wrap_agent_call(self, agent_name: str, operation: Callable, 
                              *args, **kwargs) -> Tuple[bool, Any]:
        """Wrap an agent call with error recovery."""
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                async with self.error_recovery.monitored_execution(agent_name, str(operation)):
                    result = await operation(*args, **kwargs)
                    return True, result
                    
            except Exception as e:
                # Create failure context
                context = FailureContext(
                    failure_type=self.error_recovery.classify_failure(str(e), agent_name),
                    error_message=str(e),
                    tool_name=agent_name,
                    retry_count=retry_count
                )
                
                # Handle failure
                recovery_result = await self.error_recovery.handle_failure_with_learning(context)
                
                if recovery_result.retry_suggested:
                    retry_count += 1
                    # Wait if specified
                    if 'retry_after' in recovery_result.alternative_action:
                        wait_time = int(recovery_result.alternative_action.split('_')[-2])
                        await asyncio.sleep(wait_time)
                    continue
                
                # Return recovery result
                return False, recovery_result
        
        # Max retries exceeded
        return False, FallbackResult(
            success=False,
            strategy_used=FallbackStrategy.HUMAN_READABLE_ERROR,
            user_message=f"Operation failed after {max_retries} attempts"
        )


def create_error_recovery_decorator(error_recovery: EnhancedErrorRecoverySystem):
    """Create a decorator for automatic error recovery."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            middleware = ErrorRecoveryMiddleware(error_recovery)
            # Extract agent name from function or class
            agent_name = getattr(func, '__qualname__', func.__name__)
            return await middleware.wrap_agent_call(agent_name, func, *args, **kwargs)
        return wrapper
    return decorator