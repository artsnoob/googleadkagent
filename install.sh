#!/bin/bash

# Google ADK Agent Installation Script
# This script sets up the 'agent' command for system-wide access

echo "Google ADK Agent - System-wide Installation"
echo "==========================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_SCRIPT="$SCRIPT_DIR/agent"

# Check if the agent script exists
if [ ! -f "$AGENT_SCRIPT" ]; then
    echo "Error: Agent script not found at $AGENT_SCRIPT"
    exit 1
fi

# Determine the shell configuration file
SHELL_NAME=$(basename "$SHELL")
if [ "$SHELL_NAME" = "zsh" ]; then
    CONFIG_FILE="$HOME/.zshrc"
elif [ "$SHELL_NAME" = "bash" ]; then
    if [ -f "$HOME/.bash_profile" ]; then
        CONFIG_FILE="$HOME/.bash_profile"
    else
        CONFIG_FILE="$HOME/.bashrc"
    fi
else
    echo "Warning: Unknown shell ($SHELL_NAME). Defaulting to .bashrc"
    CONFIG_FILE="$HOME/.bashrc"
fi

echo ""
echo "Choose installation method:"
echo "1) Add to PATH via shell configuration (recommended)"
echo "2) Create symlink in /usr/local/bin (requires sudo)"
echo "3) Show manual installation instructions"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Adding agent to PATH in $CONFIG_FILE..."
        
        # Check if the PATH export already exists
        if grep -q "export PATH=\"$SCRIPT_DIR:\$PATH\"" "$CONFIG_FILE" 2>/dev/null; then
            echo "Agent is already in PATH!"
        else
            echo "" >> "$CONFIG_FILE"
            echo "# Google ADK Agent" >> "$CONFIG_FILE"
            echo "export PATH=\"$SCRIPT_DIR:\$PATH\"" >> "$CONFIG_FILE"
            echo "Successfully added to PATH!"
        fi
        
        echo ""
        echo "Installation complete! Please run:"
        echo "  source $CONFIG_FILE"
        echo ""
        echo "Or restart your terminal, then you can use:"
        echo "  agent \"what is the weather in rotterdam\""
        ;;
    
    2)
        echo ""
        echo "Creating symlink in /usr/local/bin..."
        
        # Check if /usr/local/bin exists
        if [ ! -d "/usr/local/bin" ]; then
            echo "Creating /usr/local/bin directory..."
            sudo mkdir -p /usr/local/bin
        fi
        
        # Create symlink
        sudo ln -sf "$AGENT_SCRIPT" /usr/local/bin/agent
        
        if [ $? -eq 0 ]; then
            echo "Successfully created symlink!"
            echo ""
            echo "You can now use:"
            echo "  agent \"what is the weather in rotterdam\""
        else
            echo "Failed to create symlink. Please try method 1 or 3."
        fi
        ;;
    
    3)
        echo ""
        echo "Manual Installation Instructions:"
        echo "================================="
        echo ""
        echo "Option A - Add to PATH:"
        echo "  1. Open your shell configuration file:"
        echo "     $CONFIG_FILE"
        echo ""
        echo "  2. Add this line at the end:"
        echo "     export PATH=\"$SCRIPT_DIR:\$PATH\""
        echo ""
        echo "  3. Reload your shell configuration:"
        echo "     source $CONFIG_FILE"
        echo ""
        echo "Option B - Create an alias:"
        echo "  1. Open your shell configuration file:"
        echo "     $CONFIG_FILE"
        echo ""
        echo "  2. Add this line at the end:"
        echo "     alias agent='$AGENT_SCRIPT'"
        echo ""
        echo "  3. Reload your shell configuration:"
        echo "     source $CONFIG_FILE"
        echo ""
        echo "Option C - Create a symlink:"
        echo "  sudo ln -s $AGENT_SCRIPT /usr/local/bin/agent"
        ;;
    
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Usage examples:"
echo "  agent \"what is the weather in rotterdam\""
echo "  agent -m claude-3-5-sonnet \"explain quantum computing\""
echo "  agent --llm_provider openrouter --model \"openrouter/anthropic/claude-3-haiku\" \"write a haiku\""