# Agent CLI - System-Wide Command Access

This document explains how to set up and use the `agent` command from anywhere on your system.

## Installation

### Quick Installation

Run the installation script:

```bash
./install.sh
```

Choose one of the following options:
1. **Add to PATH** (recommended) - Adds the agent directory to your shell's PATH
2. **Create symlink** - Creates a symlink in /usr/local/bin (requires sudo)
3. **Manual setup** - Shows instructions for manual configuration

### Manual Installation

#### Option 1: Add to PATH

Add this line to your shell configuration file (`~/.zshrc` for zsh, `~/.bashrc` for bash):

```bash
export PATH="/Users/milanboonstra/code/googleadkagent:$PATH"
```

Then reload your shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

#### Option 2: Create an Alias

Add this line to your shell configuration file:

```bash
alias agent='/Users/milanboonstra/code/googleadkagent/agent'
```

#### Option 3: Use the Aliases File

Source the provided aliases file in your shell configuration:

```bash
source /Users/milanboonstra/code/googleadkagent/agent_aliases.sh
```

This provides additional shortcuts like `agent-claude`, `agent-gemini`, etc.

## Usage

### Direct Query Mode

Send a single query to the agent and get a response:

```bash
# Basic query
agent "what is the weather in rotterdam"

# With specific model (shorthand)
agent -m claude-3-5-sonnet "explain quantum computing"

# With specific model (full syntax)
agent --model_name gemini-2.5-flash-preview-05-20 "write a haiku about coding"

# Using OpenRouter
agent --llm_provider openrouter --model "openrouter/anthropic/claude-3-haiku" "hello world"
```

### Interactive Mode

Start an interactive session:

```bash
# Default model
agent

# With specific model
agent -m claude-3-5-sonnet

# With OpenRouter
agent --llm_provider openrouter --model "openrouter/anthropic/claude-3-haiku"
```

### Command-Line Options

- `-q, --query`: Direct query to send to the agent (non-interactive mode)
- `-m, --model`: Shorthand for --model_name
- `--model_name`: Full model name specification
- `--llm_provider`: Choose between "gemini" (default) or "openrouter"

### Examples

```bash
# Quick math
agent -q "What is 15% of 240?"

# Code generation
agent "write a Python function to calculate fibonacci numbers"

# Using Claude via OpenRouter
agent --llm_provider openrouter -m "openrouter/anthropic/claude-3-5-sonnet" "explain Docker in simple terms"

# Interactive session with specific model
agent -m gemini-2.5-flash-preview-05-20
```

### Aliases (if using agent_aliases.sh)

- `agent-claude`: Uses Claude 3.5 Sonnet via OpenRouter
- `agent-haiku`: Uses Claude 3 Haiku via OpenRouter  
- `agent-gemini`: Uses Gemini 2.5 Flash
- `agent-gpt4`: Uses GPT-4 via OpenRouter
- `agent-chat`: Starts interactive mode with default model

## Requirements

- Python 3.8+
- Virtual environment with dependencies installed
- API keys configured in .env file:
  - `GEMINI_API_KEY` for Gemini models
  - `OPENROUTER_API_KEY` for OpenRouter models
  - Other API keys as needed for MCP servers

## Troubleshooting

1. **Command not found**: Make sure you've run the installation script and reloaded your shell
2. **Permission denied**: Make sure the agent script is executable: `chmod +x agent`
3. **Virtual environment errors**: Ensure the venv is properly set up in the project directory
4. **API errors**: Check that your .env file contains the necessary API keys