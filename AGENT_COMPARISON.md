# Google ADK Agent - Classic vs Enhanced Version

## Overview

This project now includes two versions of the agent:

1. **Classic Agent** (`main.py`) - The original implementation
2. **Enhanced Agent** (`main_refactored.py`) - The improved version with advanced features

## How to Run

```bash
# Classic Agent
python main.py

# Enhanced Agent  
python main_refactored.py

# Both support the same command-line arguments:
python main.py --llm_provider openrouter --model_name openrouter/anthropic/claude-3-haiku
```

## Key Differences

### Classic Agent (`main.py`)
- ✅ Stable and tested
- ✅ Simple, straightforward implementation
- ❌ Limited error recovery
- ❌ Basic token management
- ❌ No learning capabilities
- ❌ Reactive only (waits for instructions)

### Enhanced Agent (`main_refactored.py`)
- ✅ **Smart Token Management**: Predicts token usage, prioritizes context
- ✅ **Enhanced Error Recovery**: Circuit breakers, learning from failures
- ✅ **Autonomous Behavior**: Proactive suggestions, pattern recognition
- ✅ **Intelligent Conversations**: Tracks patterns, suggests optimizations
- ✅ **Task Planning**: Breaks complex tasks into parallel subtasks
- ✅ **Extensible Architecture**: Easy to add new agents and capabilities
- ✅ **Better Code Organization**: Clean separation of concerns

## Feature Comparison

| Feature | Classic | Enhanced |
|---------|---------|----------|
| Basic functionality | ✅ | ✅ |
| Error handling | Basic | Advanced with fallbacks |
| Token management | Reactive | Predictive |
| Agent behavior | Follows instructions | Proactive & creative |
| Code organization | Monolithic | Modular |
| Learning | ❌ | ✅ Learns from patterns |
| Task planning | ❌ | ✅ Automatic decomposition |
| Conversation insights | ❌ | ✅ Pattern recognition |
| Extensibility | Limited | Plugin architecture |

## Enhanced Agent Special Features

### 1. Autonomous Problem Solving
The enhanced agents will:
- Try multiple approaches when the primary method fails
- Generate custom Python scripts for tasks without existing tools
- Suggest workflow improvements based on usage patterns
- Learn from successful solutions and apply them to similar tasks

### 2. Smart Context Management
- Predicts how many tokens a task will need
- Prioritizes conversation history based on relevance
- Automatically manages context window to prevent overflow
- Provides token usage insights and suggestions

### 3. Intelligent Error Recovery
- Circuit breaker pattern prevents repeated failures
- Learns which fallback strategies work best
- Provides helpful suggestions when things go wrong
- Monitors service health and adapts accordingly

### 4. Conversation Intelligence
- Recognizes patterns in your requests
- Suggests automations for repetitive tasks
- Tracks conversation phases and optimizes responses
- Provides metrics and improvement suggestions

## When to Use Each Version

### Use Classic Agent When:
- You need maximum stability
- You're debugging issues
- You prefer simpler, more predictable behavior
- You don't need advanced features

### Use Enhanced Agent When:
- You want the agent to be more autonomous
- You're doing complex, multi-step tasks
- You want learning and optimization features
- You need better error recovery
- You want proactive suggestions

## Migration Notes

Both versions use the same:
- Environment variables
- MCP server configurations
- File locations
- Command-line arguments

You can switch between them at any time without any configuration changes.

## Future Development

The enhanced version is designed to be extended with:
- New agent types (via plugin system)
- Custom task planners
- Additional learning algorithms
- More sophisticated conversation patterns
- Integration with external services

The classic version will be maintained for stability but won't receive new features.