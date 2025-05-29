"""
Abstract base classes for extensible agent architecture.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum
from google.genai import types

from .error_recovery_system import FallbackResult, FailureContext


class AgentType(Enum):
    """Types of agents in the system."""
    FILESYSTEM = "filesystem"
    SEARCH = "search"
    CODE_EXECUTOR = "code_executor"
    CONTENT_SCRAPER = "content_scraper"
    FETCH = "fetch"
    PERPLEXITY = "perplexity"
    TELEGRAM = "telegram"
    ROOT = "root"
    CUSTOM = "custom"


@dataclass
class AgentRequest:
    """Standard request format for agents."""
    task: str
    context: Dict[str, Any] = None
    priority: int = 1
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = None


@dataclass
class AgentResponse:
    """Standard response format from agents."""
    success: bool
    result: Any
    agent_name: str
    execution_time: float
    tokens_used: int = 0
    error: Optional[str] = None
    suggestions: List[str] = None
    metadata: Dict[str, Any] = None


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, agent_type: AgentType, 
                 model_config: Any, tools: List[Any] = None):
        self.name = name
        self.agent_type = agent_type
        self.model_config = model_config
        self.tools = tools or []
        self.capabilities: List[str] = []
        self.fallback_agents: List[str] = []
    
    @abstractmethod
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process a request and return a response."""
        pass
    
    @abstractmethod
    def can_handle(self, task: str) -> bool:
        """Determine if this agent can handle a specific task."""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        return self.capabilities
    
    def suggest_alternatives(self, task: str) -> List[str]:
        """Suggest alternative agents for a task."""
        return self.fallback_agents


class AutonomousAgent(BaseAgent):
    """Enhanced base class for autonomous agents with proactive capabilities."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learning_enabled = True
        self.task_history: List[AgentRequest] = []
        self.success_patterns: Dict[str, float] = {}
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process request with autonomous enhancements."""
        # Record task
        self.task_history.append(request)
        
        # Check for learned patterns
        if self.learning_enabled:
            enhanced_request = self._enhance_request_from_patterns(request)
        else:
            enhanced_request = request
        
        # Process with core logic
        response = await self._process_core(enhanced_request)
        
        # Learn from outcome
        if self.learning_enabled:
            self._learn_from_outcome(request, response)
        
        # Add proactive suggestions
        if response.success:
            response.suggestions = self._generate_suggestions(request, response)
        
        return response
    
    @abstractmethod
    async def _process_core(self, request: AgentRequest) -> AgentResponse:
        """Core processing logic to be implemented by subclasses."""
        pass
    
    def _enhance_request_from_patterns(self, request: AgentRequest) -> AgentRequest:
        """Enhance request based on learned patterns."""
        # Default implementation - can be overridden
        return request
    
    def _learn_from_outcome(self, request: AgentRequest, response: AgentResponse):
        """Learn from task execution outcome."""
        task_key = self._get_task_key(request.task)
        current_rate = self.success_patterns.get(task_key, 0.5)
        
        if response.success:
            # Increase success rate
            self.success_patterns[task_key] = min(current_rate + 0.1, 1.0)
        else:
            # Decrease success rate
            self.success_patterns[task_key] = max(current_rate - 0.1, 0.0)
    
    def _generate_suggestions(self, request: AgentRequest, 
                              response: AgentResponse) -> List[str]:
        """Generate proactive suggestions based on task completion."""
        suggestions = []
        
        # Override in subclasses for specific suggestions
        # Example suggestions:
        if 'file' in request.task.lower():
            suggestions.append("Consider creating a backup of modified files")
            suggestions.append("You might want to organize files into folders")
        
        return suggestions
    
    def _get_task_key(self, task: str) -> str:
        """Generate a key for task pattern recognition."""
        # Simple implementation - can be made more sophisticated
        keywords = ['create', 'read', 'write', 'search', 'analyze', 'fetch']
        for keyword in keywords:
            if keyword in task.lower():
                return keyword
        return 'general'


class AgentRegistry:
    """Registry for managing and discovering agents."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.type_registry: Dict[AgentType, List[str]] = {}
    
    def register(self, agent: BaseAgent):
        """Register an agent."""
        self.agents[agent.name] = agent
        
        # Register by type
        if agent.agent_type not in self.type_registry:
            self.type_registry[agent.agent_type] = []
        self.type_registry[agent.agent_type].append(agent.name)
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get agent by name."""
        return self.agents.get(name)
    
    def find_agents_for_task(self, task: str) -> List[BaseAgent]:
        """Find agents that can handle a specific task."""
        capable_agents = []
        for agent in self.agents.values():
            if agent.can_handle(task):
                capable_agents.append(agent)
        
        # Sort by capability match score if implemented
        return capable_agents
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[BaseAgent]:
        """Get all agents of a specific type."""
        agent_names = self.type_registry.get(agent_type, [])
        return [self.agents[name] for name in agent_names if name in self.agents]


class AgentFactory(ABC):
    """Abstract factory for creating agents."""
    
    @abstractmethod
    def create_agent(self, agent_type: AgentType, 
                     model_config: Any, tools: List[Any]) -> BaseAgent:
        """Create an agent of the specified type."""
        pass


class PluginAgent(BaseAgent):
    """Base class for plugin-based agents that can be dynamically loaded."""
    
    def __init__(self, *args, plugin_config: Dict[str, Any] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_config = plugin_config or {}
        self._load_plugin()
    
    @abstractmethod
    def _load_plugin(self):
        """Load plugin-specific configuration and capabilities."""
        pass
    
    def reload_plugin(self):
        """Reload plugin configuration."""
        self._load_plugin()


class CompositeAgent(BaseAgent):
    """Agent that combines multiple sub-agents for complex tasks."""
    
    def __init__(self, name: str, sub_agents: List[BaseAgent], *args, **kwargs):
        super().__init__(name, AgentType.CUSTOM, *args, **kwargs)
        self.sub_agents = sub_agents
        self.coordination_strategy = self._default_coordination
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process request by coordinating sub-agents."""
        # Decompose task
        sub_tasks = self._decompose_task(request.task)
        
        # Execute with coordination strategy
        results = await self.coordination_strategy(sub_tasks, self.sub_agents)
        
        # Aggregate results
        return self._aggregate_results(results, request)
    
    def can_handle(self, task: str) -> bool:
        """Check if any sub-agent can handle the task."""
        return any(agent.can_handle(task) for agent in self.sub_agents)
    
    def _decompose_task(self, task: str) -> List[str]:
        """Decompose task into sub-tasks."""
        # Default implementation - override for specific decomposition
        return [task]
    
    async def _default_coordination(self, tasks: List[str], 
                                    agents: List[BaseAgent]) -> List[AgentResponse]:
        """Default coordination strategy - sequential execution."""
        results = []
        for task in tasks:
            # Find capable agent
            for agent in agents:
                if agent.can_handle(task):
                    request = AgentRequest(task=task)
                    response = await agent.process_request(request)
                    results.append(response)
                    break
        return results
    
    def _aggregate_results(self, results: List[AgentResponse], 
                           original_request: AgentRequest) -> AgentResponse:
        """Aggregate results from sub-agents."""
        # Simple aggregation - can be overridden
        success = all(r.success for r in results)
        combined_result = {
            'sub_results': [r.result for r in results],
            'sub_agents': [r.agent_name for r in results]
        }
        
        return AgentResponse(
            success=success,
            result=combined_result,
            agent_name=self.name,
            execution_time=sum(r.execution_time for r in results),
            tokens_used=sum(r.tokens_used for r in results)
        )


class AgentOrchestrator:
    """Orchestrates complex multi-agent workflows."""
    
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.workflow_templates: Dict[str, List[Dict]] = {}
    
    def register_workflow(self, name: str, steps: List[Dict]):
        """Register a workflow template."""
        self.workflow_templates[name] = steps
    
    async def execute_workflow(self, workflow_name: str, 
                               initial_input: Any) -> Dict[str, Any]:
        """Execute a registered workflow."""
        if workflow_name not in self.workflow_templates:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        
        steps = self.workflow_templates[workflow_name]
        current_input = initial_input
        results = []
        
        for step in steps:
            agent_name = step['agent']
            task = step['task'].format(input=current_input)
            
            agent = self.registry.get_agent(agent_name)
            if not agent:
                raise ValueError(f"Agent '{agent_name}' not found")
            
            request = AgentRequest(task=task, context={'previous': current_input})
            response = await agent.process_request(request)
            
            results.append(response)
            
            if not response.success:
                # Workflow failed
                return {
                    'success': False,
                    'failed_at': agent_name,
                    'error': response.error,
                    'partial_results': results
                }
            
            # Use result as input for next step
            current_input = response.result
        
        return {
            'success': True,
            'final_result': current_input,
            'all_results': results
        }