"""
Centralized configuration management for Google ADK Agent.
Uses environment variables and provides validation.
"""
import os
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ModelConfig:
    """Configuration for LLM model."""
    provider: str = "gemini"
    name: str = "gemini-2.5-flash-preview-05-20"
    max_context_tokens: int = 1000000
    safety_margin: int = 10000
    
    def __post_init__(self):
        """Adjust context tokens based on model."""
        if "1.5" in self.name:
            self.max_context_tokens = 1000000
        elif "openrouter" in self.provider:
            self.max_context_tokens = 120000
        else:
            self.max_context_tokens = 120000

@dataclass
class PathConfig:
    """Centralized path configuration."""
    base_dir: Path = field(default_factory=lambda: Path.home() / ".config" / "adk-agent")
    data_dir: Path = field(default_factory=lambda: Path("data"))
    agent_files_dir: Path = field(default_factory=lambda: Path("data") / "agent_files")
    conversation_exports_dir: Path = field(default_factory=lambda: Path("data") / "conversation_exports")
    
    def __post_init__(self):
        """Ensure all directories exist."""
        for dir_path in [self.data_dir, self.agent_files_dir, self.conversation_exports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""
    name: str
    command: str
    args: list = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    working_dir: Optional[str] = None

@dataclass
class AgentConfig:
    """Main configuration class for the agent."""
    model: ModelConfig = field(default_factory=ModelConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    mcp_servers: Dict[str, MCPServerConfig] = field(default_factory=dict)
    
    # Feature flags
    enable_error_recovery: bool = True
    enable_token_management: bool = True
    enable_conversation_logging: bool = True
    enable_proactive_suggestions: bool = False  # New feature flag
    
    # UI settings
    show_loading_indicator: bool = True
    show_token_stats: bool = True
    
    @classmethod
    def from_env(cls) -> 'AgentConfig':
        """Create configuration from environment variables."""
        config = cls()
        
        # Model configuration from env
        if os.getenv("ADK_LLM_PROVIDER"):
            config.model.provider = os.getenv("ADK_LLM_PROVIDER")
        if os.getenv("ADK_MODEL_NAME"):
            config.model.name = os.getenv("ADK_MODEL_NAME")
        
        # Feature flags from env
        config.enable_error_recovery = os.getenv("ADK_ENABLE_ERROR_RECOVERY", "true").lower() == "true"
        config.enable_token_management = os.getenv("ADK_ENABLE_TOKEN_MANAGEMENT", "true").lower() == "true"
        config.enable_conversation_logging = os.getenv("ADK_ENABLE_CONVERSATION_LOGGING", "true").lower() == "true"
        config.enable_proactive_suggestions = os.getenv("ADK_ENABLE_PROACTIVE_SUGGESTIONS", "false").lower() == "true"
        
        # MCP servers configuration
        config._load_mcp_servers()
        
        return config
    
    def _load_mcp_servers(self):
        """Load MCP server configurations."""
        # Default MCP servers - these should be loaded from a config file or env
        self.mcp_servers = {
            "filesystem": MCPServerConfig(
                name="filesystem",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem"],
                working_dir=str(Path.home() / "dev")
            ),
            "docs": MCPServerConfig(
                name="docs",
                command="npx",
                args=["-y", "@arabold/docs-mcp-server@latest"],
                env={
                    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
                    "DOCS_STORAGE_PATH": str(self.paths.base_dir / "indexed-docs")
                }
            ),
            "telegram": MCPServerConfig(
                name="telegram",
                command="python",
                args=[str(Path(__file__).parent.parent / "mcp" / "telegram_mcp_server.py")],
                env={
                    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", ""),
                    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID", "")
                }
            )
        }
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of warnings."""
        warnings = []
        
        # Check API keys
        if self.model.provider == "openrouter" and not os.getenv("OPENROUTER_API_KEY"):
            warnings.append("OpenRouter selected but OPENROUTER_API_KEY not set")
        
        if not os.getenv("GOOGLE_API_KEY") and self.model.provider == "gemini":
            warnings.append("Gemini selected but GOOGLE_API_KEY not set")
        
        # Check MCP server requirements
        for name, server in self.mcp_servers.items():
            if name == "telegram" and not server.env.get("TELEGRAM_BOT_TOKEN"):
                warnings.append(f"Telegram MCP server configured but TELEGRAM_BOT_TOKEN not set")
            elif name == "docs" and not server.env.get("OPENAI_API_KEY"):
                warnings.append(f"Docs MCP server configured but OPENAI_API_KEY not set")
        
        return warnings


# Singleton instance
_config: Optional[AgentConfig] = None

def get_config() -> AgentConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = AgentConfig.from_env()
    return _config

def reset_config():
    """Reset the configuration (useful for testing)."""
    global _config
    _config = None