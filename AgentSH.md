# AgentSH - Shell Integration for Google ADK Agent

## Overview
AgentSH provides system-wide shell access to the Google ADK Agent, allowing you to run AI queries from anywhere in your terminal.

## Quick Start
```bash
# Install AgentSH
./install.sh

# Use from anywhere
agent "what is the weather in rotterdam"
```

## Components
- **`/agent`** - Core shell wrapper that manages environment activation
- **`/install.sh`** - Automated installer for shell integration
- **`/agent_aliases.sh`** - Model-specific command shortcuts

## Features
- Run agent queries from any directory
- Automatic virtual environment management
- Smart argument parsing (queries don't need `-q` flag)
- Pre-configured model aliases

## Installation Methods
1. **PATH Integration** - Adds agent to your shell's PATH
2. **Symlink** - Creates `/usr/local/bin/agent` link
3. **Manual** - DIY configuration options

## Usage Examples
```bash
# Direct query
agent "explain quantum computing"

# Interactive mode
agent

# With specific model
agent -m claude-3-5-sonnet "write a haiku"

# Using aliases (after sourcing agent_aliases.sh)
agent-claude "your query"
agent-gemini "your query"
```

AgentSH makes AI assistance just one command away, no matter where you are in your filesystem.