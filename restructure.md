# Google ADK Agent Directory Restructure Plan

## Current Issues
- All Python modules scattered in root directory
- Documentation files mixed with code
- Nested `agent_files/agent_files/` structure
- No logical grouping of related components

## Proposed Directory Structure

```
googleadkagent/
├── src/                          # Main source code
│   ├── core/                     # Core system components
│   │   ├── __init__.py
│   │   ├── mcp_agent.py         # Main entry point
│   │   ├── token_manager.py     # Context window management
│   │   └── error_recovery_system.py
│   ├── agents/                   # Agent configuration and logic
│   │   ├── __init__.py
│   │   └── agent_config.py      # All agent definitions
│   ├── mcp/                      # MCP server management
│   │   ├── __init__.py
│   │   └── mcp_server_init.py   # MCP initialization
│   ├── processors/               # Event and data processing
│   │   ├── __init__.py
│   │   ├── event_processor.py   # Response handling
│   │   └── conversation_logger.py
│   ├── utils/                    # Utilities and formatters
│   │   ├── __init__.py
│   │   ├── mcp_agent_utils.py   # UI utilities
│   │   └── telegram_formatter.py
│   └── __init__.py
├── docs/                         # All documentation
│   ├── README.md
│   ├── PROJECT_STRUCTURE.md
│   ├── adk_docs.md
│   ├── config.md
│   └── agent_development_status.md
├── data/                         # Data and working files
│   ├── agent_files/             # Agent working directory
│   └── conversation_exports/    # Conversation logs
├── config/                       # Configuration files
│   ├── CLAUDE.md
│   └── requirements.txt
├── venv/                         # Virtual environment (unchanged)
└── error.md                     # Keep at root for now
```

## Benefits of This Structure

### Clear Separation of Concerns
- **src/core/** - Core system components (main entry, token management, error recovery)
- **src/agents/** - Agent configuration and logic
- **src/mcp/** - MCP server management
- **src/processors/** - Event and data processing
- **src/utils/** - Utilities and formatters

### Logical Grouping
- Related functionality is grouped together
- Easy to find specific components
- Reduces cognitive overhead when navigating

### Documentation Centralization
- All documentation files in `docs/` directory
- Clear separation from code
- Better organization for project documentation

### Data Isolation
- Working files separate from source code
- Clear distinction between generated and source content
- Agent files and conversation exports properly organized

### Python Package Structure
- Proper `__init__.py` files for clean imports
- Follows Python packaging conventions
- Enables better module organization

## File Movements Required

### From Root to src/core/
- `mcp_agent.py`
- `token_manager.py`
- `error_recovery_system.py`

### From Root to src/agents/
- `agent_config.py`

### From Root to src/mcp/
- `mcp_server_init.py`

### From Root to src/processors/
- `event_processor.py`
- `conversation_logger.py`

### From Root to src/utils/
- `mcp_agent_utils.py`
- `telegram_formatter.py`

### From Root to docs/
- `README.md`
- `PROJECT_STRUCTURE.md`
- `adk_docs.md`
- `config.md`
- `agent_development_status.md`

### From Root to config/
- `CLAUDE.md`
- `requirements.txt`

### Rename/Reorganize
- `agent_files/` → `data/agent_files/`
- `conversation_exports/` → `data/conversation_exports/`

## Import Updates Required

After restructuring, import statements will need to be updated:

### In mcp_agent.py (src/core/mcp_agent.py):
```python
# From:
from mcp_agent_utils import ...
from token_manager import TokenManager
from error_recovery_system import ErrorRecoverySystem
from mcp_server_init import initialize_all_mcp_servers
from agent_config import create_all_agents
from event_processor import process_events
from conversation_logger import ConversationLogger

# To:
from ..utils.mcp_agent_utils import ...
from .token_manager import TokenManager
from .error_recovery_system import ErrorRecoverySystem
from ..mcp.mcp_server_init import initialize_all_mcp_servers
from ..agents.agent_config import create_all_agents
from ..processors.event_processor import process_events
from ..processors.conversation_logger import ConversationLogger
```

### Similar updates needed in other files based on their new locations.

## Implementation Steps

1. Create new directory structure
2. Move files to appropriate locations
3. Create `__init__.py` files for Python packages
4. Update all import statements
5. Update any hardcoded paths in configuration
6. Test the application to ensure everything works
7. Update documentation references to reflect new structure

This restructure will make the codebase much more maintainable and professional while following Python best practices.