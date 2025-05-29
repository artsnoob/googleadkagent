"""
Task planning system for breaking down complex requests into executable steps.
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re


class TaskPriority(Enum):
    """Priority levels for tasks."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class SubTask:
    """Represents a single subtask in a plan."""
    id: str
    description: str
    agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    estimated_tokens: int = 1000
    retry_count: int = 0
    max_retries: int = 3
    fallback_approach: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class ExecutionPlan:
    """Represents a complete execution plan for a user request."""
    request: str
    subtasks: List[SubTask]
    total_estimated_tokens: int = 0
    parallel_groups: List[List[str]] = field(default_factory=list)
    
    def __post_init__(self):
        """Calculate total tokens and identify parallel execution groups."""
        self.total_estimated_tokens = sum(task.estimated_tokens for task in self.subtasks)
        self._identify_parallel_groups()
    
    def _identify_parallel_groups(self):
        """Identify which tasks can be executed in parallel."""
        # Build dependency graph
        task_map = {task.id: task for task in self.subtasks}
        
        # Group tasks by dependency level
        levels = {}
        for task in self.subtasks:
            level = self._get_dependency_level(task.id, task_map)
            if level not in levels:
                levels[level] = []
            levels[level].append(task.id)
        
        # Convert to parallel groups
        self.parallel_groups = [levels[level] for level in sorted(levels.keys())]
    
    def _get_dependency_level(self, task_id: str, task_map: Dict[str, SubTask]) -> int:
        """Get the dependency level of a task (0 = no dependencies)."""
        task = task_map[task_id]
        if not task.dependencies:
            return 0
        
        max_level = 0
        for dep_id in task.dependencies:
            if dep_id in task_map:
                dep_level = self._get_dependency_level(dep_id, task_map)
                max_level = max(max_level, dep_level)
        
        return max_level + 1


class TaskPlanner:
    """Intelligent task planner for breaking down complex requests."""
    
    def __init__(self):
        self.task_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize common task patterns."""
        return {
            'research_and_report': {
                'pattern': r'(research|find|investigate|analyze).*(report|summary|document)',
                'subtasks': [
                    ('research', 'search_agent', TaskPriority.HIGH),
                    ('deep_dive', 'perplexity_agent', TaskPriority.HIGH),
                    ('compile_report', 'code_executor_agent', TaskPriority.MEDIUM),
                    ('save_report', 'filesystem_agent', TaskPriority.MEDIUM)
                ]
            },
            'web_scraping_workflow': {
                'pattern': r'(scrape|extract|collect).*(web|site|url)',
                'subtasks': [
                    ('fetch_content', 'fetch_agent', TaskPriority.HIGH),
                    ('parse_data', 'code_executor_agent', TaskPriority.HIGH),
                    ('save_results', 'filesystem_agent', TaskPriority.MEDIUM),
                    ('analyze_data', 'code_executor_agent', TaskPriority.LOW)
                ]
            },
            'ai_news_workflow': {
                'pattern': r'(ai news|latest ai|artificial intelligence news)',
                'subtasks': [
                    ('scrape_reddit', 'content_scraper_agent', TaskPriority.HIGH),
                    ('fetch_rss', 'content_scraper_agent', TaskPriority.HIGH),
                    ('aggregate_news', 'code_executor_agent', TaskPriority.MEDIUM),
                    ('send_telegram', 'telegram_agent', TaskPriority.MEDIUM)
                ]
            },
            'data_analysis': {
                'pattern': r'(analyze|process|visualize).*(data|csv|json|file)',
                'subtasks': [
                    ('load_data', 'filesystem_agent', TaskPriority.HIGH),
                    ('process_data', 'code_executor_agent', TaskPriority.HIGH),
                    ('visualize', 'code_executor_agent', TaskPriority.MEDIUM),
                    ('save_results', 'filesystem_agent', TaskPriority.MEDIUM)
                ]
            },
            'automation_workflow': {
                'pattern': r'(automate|schedule|monitor)',
                'subtasks': [
                    ('analyze_task', 'code_executor_agent', TaskPriority.HIGH),
                    ('create_script', 'code_executor_agent', TaskPriority.HIGH),
                    ('test_script', 'code_executor_agent', TaskPriority.MEDIUM),
                    ('save_script', 'filesystem_agent', TaskPriority.MEDIUM),
                    ('setup_schedule', 'code_executor_agent', TaskPriority.LOW)
                ]
            }
        }
    
    def decompose_task(self, user_request: str) -> List[SubTask]:
        """Break down a user request into subtasks."""
        # Check for matching patterns
        for workflow_name, workflow in self.task_patterns.items():
            if re.search(workflow['pattern'], user_request.lower()):
                return self._create_subtasks_from_pattern(workflow, user_request)
        
        # If no pattern matches, use intelligent decomposition
        return self._intelligent_decomposition(user_request)
    
    def _create_subtasks_from_pattern(self, workflow: Dict[str, Any], 
                                      request: str) -> List[SubTask]:
        """Create subtasks from a workflow pattern."""
        subtasks = []
        for i, (task_desc, agent, priority) in enumerate(workflow['subtasks']):
            task = SubTask(
                id=f"task_{i+1}",
                description=task_desc,
                agent=agent,
                priority=priority,
                dependencies=[f"task_{i}"] if i > 0 else [],
                fallback_approach=self._get_fallback_approach(agent)
            )
            subtasks.append(task)
        
        return subtasks
    
    def _intelligent_decomposition(self, request: str) -> List[SubTask]:
        """Intelligently decompose a request without a pattern."""
        subtasks = []
        
        # Analyze request for key actions
        actions = self._extract_actions(request)
        
        for i, action in enumerate(actions):
            agent = self._determine_agent_for_action(action)
            task = SubTask(
                id=f"task_{i+1}",
                description=action,
                agent=agent,
                priority=TaskPriority.MEDIUM,
                dependencies=[f"task_{i}"] if i > 0 else [],
                fallback_approach=self._get_fallback_approach(agent)
            )
            subtasks.append(task)
        
        return subtasks
    
    def _extract_actions(self, request: str) -> List[str]:
        """Extract actionable items from a request."""
        # Simple action extraction based on verbs
        action_verbs = [
            'create', 'write', 'read', 'analyze', 'fetch', 'download',
            'search', 'find', 'process', 'convert', 'save', 'send',
            'calculate', 'generate', 'extract', 'compile', 'run'
        ]
        
        actions = []
        words = request.lower().split()
        
        for i, word in enumerate(words):
            for verb in action_verbs:
                if word.startswith(verb):
                    # Extract the action phrase
                    action_phrase = ' '.join(words[i:min(i+5, len(words))])
                    actions.append(action_phrase)
                    break
        
        # If no actions found, create a generic task
        if not actions:
            actions = [request]
        
        return actions
    
    def _determine_agent_for_action(self, action: str) -> str:
        """Determine the best agent for an action."""
        action_lower = action.lower()
        
        # Agent mapping based on keywords
        agent_map = {
            'filesystem_agent': ['file', 'directory', 'save', 'read', 'write', 'create', 'delete'],
            'search_agent': ['search', 'google', 'find online', 'research'],
            'code_executor_agent': ['code', 'script', 'calculate', 'process', 'analyze', 'generate'],
            'fetch_agent': ['fetch', 'download', 'url', 'website', 'webpage'],
            'content_scraper_agent': ['reddit', 'twitter', 'rss', 'news', 'social'],
            'perplexity_agent': ['deep research', 'comprehensive', 'expert', 'detailed analysis'],
            'telegram_agent': ['telegram', 'send message', 'notify']
        }
        
        for agent, keywords in agent_map.items():
            for keyword in keywords:
                if keyword in action_lower:
                    return agent
        
        # Default to code executor for unknown tasks
        return 'code_executor_agent'
    
    def _get_fallback_approach(self, agent: str) -> str:
        """Get fallback approach for an agent."""
        fallbacks = {
            'filesystem_agent': 'Use code_executor_agent with os/pathlib',
            'search_agent': 'Use fetch_agent with search engine URLs',
            'fetch_agent': 'Use code_executor_agent with requests library',
            'content_scraper_agent': 'Use fetch_agent or code_executor_agent with BeautifulSoup',
            'perplexity_agent': 'Use search_agent with multiple queries',
            'telegram_agent': 'Save message to file for manual sending'
        }
        return fallbacks.get(agent, 'Use code_executor_agent to create custom solution')
    
    def create_execution_plan(self, subtasks: List[SubTask], request: str) -> ExecutionPlan:
        """Create an optimized execution plan."""
        # Optimize task order based on dependencies and priority
        optimized_tasks = self._optimize_task_order(subtasks)
        
        return ExecutionPlan(
            request=request,
            subtasks=optimized_tasks
        )
    
    def _optimize_task_order(self, subtasks: List[SubTask]) -> List[SubTask]:
        """Optimize task execution order."""
        # Sort by priority and dependencies
        # This is a simplified topological sort
        sorted_tasks = []
        remaining = subtasks.copy()
        
        while remaining:
            # Find tasks with no pending dependencies
            ready_tasks = []
            for task in remaining:
                deps_satisfied = all(
                    dep in [t.id for t in sorted_tasks]
                    for dep in task.dependencies
                )
                if deps_satisfied:
                    ready_tasks.append(task)
            
            # Sort ready tasks by priority
            ready_tasks.sort(key=lambda t: t.priority.value)
            
            if ready_tasks:
                sorted_tasks.extend(ready_tasks)
                for task in ready_tasks:
                    remaining.remove(task)
            else:
                # Circular dependency or error - add remaining tasks
                sorted_tasks.extend(remaining)
                break
        
        return sorted_tasks
    
    def update_plan_with_result(self, plan: ExecutionPlan, task_id: str, 
                                result: Any, success: bool) -> ExecutionPlan:
        """Update plan based on task execution result."""
        for task in plan.subtasks:
            if task.id == task_id:
                if success:
                    task.status = TaskStatus.COMPLETED
                    task.result = result
                else:
                    task.status = TaskStatus.FAILED
                    task.error = str(result)
                    task.retry_count += 1
                break
        
        # Adjust remaining tasks based on failure if needed
        if not success:
            self._adjust_plan_for_failure(plan, task_id)
        
        return plan
    
    def _adjust_plan_for_failure(self, plan: ExecutionPlan, failed_task_id: str):
        """Adjust execution plan when a task fails."""
        # Find dependent tasks
        for task in plan.subtasks:
            if failed_task_id in task.dependencies and task.status == TaskStatus.PENDING:
                # Mark dependent tasks for special handling
                task.fallback_approach = f"Previous task {failed_task_id} failed. {task.fallback_approach}"


class IntelligentTaskExecutor:
    """Executes tasks with intelligent retry and fallback logic."""
    
    def __init__(self, planner: TaskPlanner):
        self.planner = planner
    
    async def execute_plan(self, plan: ExecutionPlan, agent_registry: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task plan with parallel execution where possible."""
        results = {}
        
        for parallel_group in plan.parallel_groups:
            # Execute tasks in parallel within each group
            group_results = await self._execute_parallel_group(
                parallel_group, plan, agent_registry
            )
            results.update(group_results)
        
        return {
            'success': all(task.status == TaskStatus.COMPLETED for task in plan.subtasks),
            'results': results,
            'plan': plan
        }
    
    async def _execute_parallel_group(self, task_ids: List[str], 
                                      plan: ExecutionPlan, 
                                      agent_registry: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a group of tasks in parallel."""
        # This is a placeholder - actual implementation would use asyncio.gather
        results = {}
        
        for task_id in task_ids:
            task = next(t for t in plan.subtasks if t.id == task_id)
            if task.status != TaskStatus.PENDING:
                continue
            
            # Execute task with retry logic
            success, result = await self._execute_single_task(task, agent_registry)
            
            # Update plan
            self.planner.update_plan_with_result(plan, task_id, result, success)
            results[task_id] = result
        
        return results
    
    async def _execute_single_task(self, task: SubTask, 
                                   agent_registry: Dict[str, Any]) -> Tuple[bool, Any]:
        """Execute a single task with retry and fallback."""
        # This is a placeholder for actual execution
        # In real implementation, this would call the appropriate agent
        
        # Simulate execution
        try:
            # Get the agent
            agent = agent_registry.get(task.agent)
            if not agent:
                raise ValueError(f"Agent {task.agent} not found")
            
            # Execute task (placeholder)
            result = f"Executed {task.description} with {task.agent}"
            
            return True, result
            
        except Exception as e:
            if task.retry_count < task.max_retries:
                # Retry logic would go here
                return False, str(e)
            else:
                # Use fallback approach
                return False, f"Failed after {task.max_retries} retries: {e}"