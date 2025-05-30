#!/bin/bash

# Google ADK Agent - Shell Aliases
# Source this file in your shell configuration to use agent commands

# Get the directory where this script is located
AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Main agent command
alias agent="$AGENT_DIR/agent"

# Convenient shortcuts for different models
alias agent-claude="$AGENT_DIR/agent --llm_provider openrouter --model openrouter/anthropic/claude-3-5-sonnet-20241022"
alias agent-haiku="$AGENT_DIR/agent --llm_provider openrouter --model openrouter/anthropic/claude-3-haiku"
alias agent-gemini="$AGENT_DIR/agent --llm_provider gemini --model gemini-2.5-flash-preview-05-20"
alias agent-gpt4="$AGENT_DIR/agent --llm_provider openrouter --model openrouter/openai/gpt-4o"

# Quick interactive mode
alias agent-chat="$AGENT_DIR/agent"

# Example usage:
# agent "what is the weather in rotterdam"
# agent-claude "explain quantum computing"
# agent-chat (starts interactive mode)