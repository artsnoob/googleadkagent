"""
Conversation logger for saving agent interactions to markdown files.
Tracks all user messages, agent responses, and tool calls.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import json


class ConversationLogger:
    """Handles logging and exporting of conversation history to markdown."""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.session_start = datetime.now()
        self.model_info = None
        
    def set_model_info(self, provider: str, model_name: str):
        """Set the model information for the session."""
        self.model_info = {
            "provider": provider,
            "model": model_name
        }
        
    def add_user_message(self, message: str):
        """Add a user message to the conversation history."""
        self.conversation_history.append({
            "type": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_assistant_message(self, message: str):
        """Add an assistant message to the conversation history."""
        self.conversation_history.append({
            "type": "assistant",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_tool_call(self, tool_name: str, args: Dict[str, Any], result: str):
        """Add a tool call to the conversation history."""
        self.conversation_history.append({
            "type": "tool_call",
            "tool": tool_name,
            "arguments": args,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_status_message(self, message: str, status_type: str):
        """Add a status message (info, warning, error) to the conversation history."""
        self.conversation_history.append({
            "type": "status",
            "status_type": status_type,
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_metadata(self, metadata: Dict[str, Any]):
        """Add metadata (like grounding info) to the conversation history."""
        self.conversation_history.append({
            "type": "metadata",
            "content": metadata,
            "timestamp": datetime.now().isoformat()
        })
    
    def clear(self):
        """Clear the conversation history and reset the session start time."""
        self.conversation_history = []
        self.session_start = datetime.now()
        
    def export_to_markdown(self, filename: Optional[str] = None) -> str:
        """Export the conversation to a markdown file."""
        if not filename:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.md"
            
        # Ensure the exports directory exists
        export_dir = os.path.join(os.path.dirname(__file__), "conversation_exports")
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, filename)
        
        # Build the markdown content
        md_content = self._build_markdown()
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        return filepath
        
    def _build_markdown(self) -> str:
        """Build the markdown content from conversation history."""
        lines = []
        
        # Header
        lines.append("# Agent Conversation Log")
        lines.append("")
        lines.append(f"**Session Start:** {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Export Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.model_info:
            lines.append(f"**Model Provider:** {self.model_info['provider']}")
            lines.append(f"**Model:** {self.model_info['model']}")
            
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Conversation content
        for entry in self.conversation_history:
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M:%S')
            
            if entry['type'] == 'user':
                lines.append(f"### 👤 User [{timestamp}]")
                lines.append("")
                lines.append(entry['content'])
                lines.append("")
                
            elif entry['type'] == 'assistant':
                lines.append(f"### 🤖 Assistant [{timestamp}]")
                lines.append("")
                lines.append(entry['content'])
                lines.append("")
                
            elif entry['type'] == 'tool_call':
                lines.append(f"#### 🔧 Tool Call: `{entry['tool']}` [{timestamp}]")
                lines.append("")
                lines.append("**Arguments:**")
                lines.append("```json")
                lines.append(json.dumps(entry['arguments'], indent=2))
                lines.append("```")
                lines.append("")
                lines.append("**Result:**")
                lines.append("```")
                # Truncate very long results
                result = entry['result']
                if len(result) > 5000:
                    result = result[:5000] + "\n... (truncated)"
                lines.append(result)
                lines.append("```")
                lines.append("")
                
            elif entry['type'] == 'status':
                emoji = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅"}.get(entry['status_type'], "📌")
                lines.append(f"_{emoji} {entry['content']}_ [{timestamp}]")
                lines.append("")
                
            elif entry['type'] == 'metadata':
                lines.append(f"#### 📊 Metadata [{timestamp}]")
                lines.append("```json")
                lines.append(json.dumps(entry['content'], indent=2))
                lines.append("```")
                lines.append("")
                
        # Footer
        lines.append("---")
        lines.append("")
        lines.append(f"_Exported from Google ADK Agent_")
        
        return "\n".join(lines)