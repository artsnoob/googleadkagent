"""
Enhanced event processor with handler registry pattern for cleaner, more extensible event handling.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass
import json
from enum import Enum
import re

from ..utils.mcp_agent_utils import (
    COLOR_GREEN, COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA, COLOR_RESET,
    COLOR_BLUE, COLOR_DIM, SYMBOL_SUCCESS, SYMBOL_WARNING, SYMBOL_THINKING,
    SYMBOL_TOOL, SYMBOL_SEARCH, SYMBOL_INFO, pretty_print_json_string,
    print_section_header, print_status_message, format_tool_response,
    ConversationStats
)
from ..core.error_recovery_system import ErrorRecoverySystem, create_failure_context


class EventType(Enum):
    """Types of events that can be processed."""
    TEXT_CONTENT = "text_content"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESPONSE = "function_response"
    GROUNDING_METADATA = "grounding_metadata"
    URL_CONTEXT = "url_context"
    SEARCH_SUGGESTIONS = "search_suggestions"
    GENERIC = "generic"


@dataclass
class ProcessedEvent:
    """Result of processing an event."""
    event_type: EventType
    content: Any
    display_content: str
    metadata: Dict[str, Any] = None
    should_log: bool = True


class EventHandler(ABC):
    """Abstract base class for event handlers."""
    
    @abstractmethod
    def can_handle(self, event: Any, part: Any = None) -> bool:
        """Determine if this handler can process the event/part."""
        pass
    
    @abstractmethod
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        """Process the event and return structured result."""
        pass
    
    @abstractmethod
    def get_event_type(self) -> EventType:
        """Get the type of events this handler processes."""
        pass


class TextContentHandler(EventHandler):
    """Handles text content from agent responses."""
    
    def can_handle(self, event: Any, part: Any = None) -> bool:
        return part and hasattr(part, 'text') and part.text
    
    def _clean_markdown(self, text: str) -> str:
        """Remove markdown formatting for better CLI readability."""
        # Remove bold markdown (**text** or __text__)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        
        # Remove italic markdown (*text* or _text_)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Remove inline code (`code`)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove strikethrough (~~text~~)
        text = re.sub(r'~~([^~]+)~~', r'\1', text)
        
        # Clean up any remaining orphan markers
        text = text.replace('**', '').replace('__', '').replace('~~', '')
        
        return text
    
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        print_section_header("Agent Response", width=50)
        
        # Format and display text with markdown removal
        display_lines = []
        for line in part.text.splitlines():
            # Clean markdown for better readability
            cleaned_line = self._clean_markdown(line)
            
            formatted_line = f"{COLOR_GREEN}{cleaned_line}{COLOR_RESET}"
            print(formatted_line)
            display_lines.append(formatted_line)
        
        print()  # Add blank line for separation
        
        return ProcessedEvent(
            event_type=EventType.TEXT_CONTENT,
            content=part.text,
            display_content="\n".join(display_lines),
            metadata={"line_count": len(display_lines)}
        )
    
    def get_event_type(self) -> EventType:
        return EventType.TEXT_CONTENT


class FunctionCallHandler(EventHandler):
    """Handles function/tool calls."""
    
    def __init__(self):
        self.pending_calls: Dict[str, Dict] = {}
    
    def can_handle(self, event: Any, part: Any = None) -> bool:
        return part and hasattr(part, 'function_call') and part.function_call
    
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        func_call = part.function_call
        print_section_header(f"Tool Call: {func_call.name}", width=50)
        
        # Parse and display arguments
        try:
            args_dict = json.loads(func_call.args)
            pretty_print_json_string(func_call.args, COLOR_YELLOW)
        except:
            args_dict = {"raw_args": func_call.args}
            print(f"{COLOR_YELLOW}{func_call.args}{COLOR_RESET}")
        
        print()  # Add blank line
        
        # Store for matching with response
        call_id = f"{func_call.name}_{id(func_call)}"
        self.pending_calls[call_id] = {
            "name": func_call.name,
            "args": args_dict
        }
        
        return ProcessedEvent(
            event_type=EventType.FUNCTION_CALL,
            content={"name": func_call.name, "args": args_dict},
            display_content=f"Calling {func_call.name} with args: {json.dumps(args_dict, indent=2)}",
            metadata={"call_id": call_id}
        )
    
    def get_event_type(self) -> EventType:
        return EventType.FUNCTION_CALL


class FunctionResponseHandler(EventHandler):
    """Handles function/tool responses."""
    
    def __init__(self, function_call_handler: Optional[FunctionCallHandler] = None):
        self.function_call_handler = function_call_handler
    
    def can_handle(self, event: Any, part: Any = None) -> bool:
        return part and hasattr(part, 'function_response') and part.function_response
    
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        func_response = part.function_response
        
        # Extract tool name
        tool_name = "UnknownTool"
        if hasattr(func_response, 'name') and func_response.name:
            tool_name = func_response.name
        
        # Extract response content
        response_data = func_response.response
        if isinstance(response_data, dict) and 'content' in response_data:
            display_content = response_data['content']
        else:
            display_content = response_data
        
        # Format and display
        format_tool_response(tool_name, display_content)
        
        # Match with pending call if available
        call_info = None
        if self.function_call_handler:
            # Find matching call
            for call_id, info in self.function_call_handler.pending_calls.items():
                if info['name'] == tool_name:
                    call_info = info
                    del self.function_call_handler.pending_calls[call_id]
                    break
        
        return ProcessedEvent(
            event_type=EventType.FUNCTION_RESPONSE,
            content={
                "tool": tool_name,
                "response": display_content,
                "call_info": call_info
            },
            display_content=str(display_content),
            metadata={"tool_name": tool_name}
        )
    
    def get_event_type(self) -> EventType:
        return EventType.FUNCTION_RESPONSE


class GroundingMetadataHandler(EventHandler):
    """Handles grounding metadata (web search queries and sources)."""
    
    def can_handle(self, event: Any, part: Any = None) -> bool:
        if not hasattr(event, 'candidates') or not event.candidates:
            return False
        
        for candidate in event.candidates:
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                return True
        return False
    
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        all_metadata = {
            "queries": [],
            "sources": []
        }
        
        for candidate in event.candidates:
            if not hasattr(candidate, 'grounding_metadata'):
                continue
                
            grounding = candidate.grounding_metadata
            
            # Handle web search queries
            if hasattr(grounding, 'web_search_queries') and grounding.web_search_queries:
                print_section_header("Web Search Queries", width=50)
                for query in grounding.web_search_queries:
                    print(f"{COLOR_CYAN}  {SYMBOL_SEARCH} {query}{COLOR_RESET}")
                    all_metadata["queries"].append(query)
                print()
            
            # Handle grounding sources
            if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                print_section_header("Grounding Sources", width=50)
                for i, chunk in enumerate(grounding.grounding_chunks):
                    title = "N/A"
                    uri = "N/A"
                    if hasattr(chunk, 'web'):
                        if hasattr(chunk.web, 'title') and chunk.web.title:
                            title = chunk.web.title
                        if hasattr(chunk.web, 'uri') and chunk.web.uri:
                            uri = chunk.web.uri
                    
                    print(f"{COLOR_CYAN}  {SYMBOL_INFO} Source {i+1}: {title[:50]}{'...' if len(title) > 50 else ''}{COLOR_RESET}")
                    print(f"{COLOR_DIM}    {uri}{COLOR_RESET}")
                    
                    all_metadata["sources"].append({
                        "title": title,
                        "uri": uri
                    })
                print()
        
        return ProcessedEvent(
            event_type=EventType.GROUNDING_METADATA,
            content=all_metadata,
            display_content=f"Found {len(all_metadata['queries'])} queries and {len(all_metadata['sources'])} sources",
            metadata=all_metadata
        )
    
    def get_event_type(self) -> EventType:
        return EventType.GROUNDING_METADATA


class URLContextHandler(EventHandler):
    """Handles URL context metadata."""
    
    def can_handle(self, event: Any, part: Any = None) -> bool:
        if not hasattr(event, 'candidates') or not event.candidates:
            return False
        
        for candidate in event.candidates:
            if hasattr(candidate, 'url_context_metadata') and candidate.url_context_metadata:
                return True
        return False
    
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        url_metadata_list = []
        
        for candidate in event.candidates:
            if not hasattr(candidate, 'url_context_metadata'):
                continue
                
            url_meta_data = candidate.url_context_metadata
            if hasattr(url_meta_data, 'url_metadata') and url_meta_data.url_metadata:
                print_section_header("URL Context Metadata", width=50)
                
                for i, meta_item in enumerate(url_meta_data.url_metadata):
                    retrieved_url = meta_item.retrieved_url if hasattr(meta_item, 'retrieved_url') else "N/A"
                    status = meta_item.url_retrieval_status if hasattr(meta_item, 'url_retrieval_status') else "N/A"
                    status_str = str(status) if status != "N/A" else "N/A"
                    status_symbol = SYMBOL_SUCCESS if "success" in status_str.lower() else SYMBOL_WARNING
                    
                    print(f"{COLOR_BLUE}  {status_symbol} URL {i+1}: {retrieved_url[:60]}{'...' if len(retrieved_url) > 60 else ''}{COLOR_RESET}")
                    print(f"{COLOR_DIM}    Status: {status_str}{COLOR_RESET}")
                    
                    url_metadata_list.append({
                        "url": retrieved_url,
                        "status": status_str
                    })
                print()
        
        return ProcessedEvent(
            event_type=EventType.URL_CONTEXT,
            content=url_metadata_list,
            display_content=f"Processed {len(url_metadata_list)} URLs",
            metadata={"url_count": len(url_metadata_list)}
        )
    
    def get_event_type(self) -> EventType:
        return EventType.URL_CONTEXT


class GenericEventHandler(EventHandler):
    """Fallback handler for unrecognized events."""
    
    def can_handle(self, event: Any, part: Any = None) -> bool:
        return True  # Always can handle as fallback
    
    async def handle(self, event: Any, part: Any = None) -> ProcessedEvent:
        print(f"{COLOR_MAGENTA}--- Event Information ---{COLOR_RESET}")
        
        try:
            event_str = str(event)
            print(f"{COLOR_MAGENTA}{event_str}{COLOR_RESET}")
            display_content = event_str
        except Exception as e:
            error_msg = f"Error displaying event: {e}"
            print(f"{COLOR_MAGENTA}{error_msg}{COLOR_RESET}")
            display_content = error_msg
        
        print()
        
        return ProcessedEvent(
            event_type=EventType.GENERIC,
            content=event,
            display_content=display_content,
            should_log=False  # Don't log generic events by default
        )
    
    def get_event_type(self) -> EventType:
        return EventType.GENERIC


class EventProcessor:
    """Main event processor with handler registry."""
    
    def __init__(self, error_recovery: ErrorRecoverySystem, 
                 conversation_logger=None, stats: ConversationStats = None):
        self.error_recovery = error_recovery
        self.conversation_logger = conversation_logger
        self.stats = stats
        self.handlers: List[EventHandler] = []
        self._initialize_handlers()
    
    def _initialize_handlers(self):
        """Initialize default handlers."""
        # Create handlers with dependencies
        func_call_handler = FunctionCallHandler()
        func_response_handler = FunctionResponseHandler(func_call_handler)
        
        # Register handlers in priority order
        self.register_handler(TextContentHandler())
        self.register_handler(func_call_handler)
        self.register_handler(func_response_handler)
        self.register_handler(GroundingMetadataHandler())
        self.register_handler(URLContextHandler())
        self.register_handler(GenericEventHandler())  # Fallback
    
    def register_handler(self, handler: EventHandler):
        """Register a new event handler."""
        self.handlers.append(handler)
    
    def unregister_handler(self, handler_type: Type[EventHandler]):
        """Remove a handler by type."""
        self.handlers = [h for h in self.handlers if not isinstance(h, handler_type)]
    
    async def process_events(self, events_async, loading_indicator=None):
        """Process events using registered handlers."""
        response_time = None
        assistant_response_parts = []
        first_event = True
        
        try:
            async for event in events_async:
                # Stop loading indicator on first event
                if first_event and loading_indicator:
                    first_event = False
                    loading_indicator.stop()
                
                # Process event parts
                if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        processed = await self._process_part(event, part)
                        if processed and processed.event_type == EventType.TEXT_CONTENT:
                            assistant_response_parts.append(processed.content)
                
                # Process event-level metadata
                await self._process_event_metadata(event)
        
        except Exception as e:
            # Enhanced error handling
            context = create_failure_context(
                e, 
                tool_name="event_processor", 
                user_intent="process_agent_response"
            )
            fallback_result = await self.error_recovery.handle_failure(context)
            
            print_status_message(
                f"Error processing response: {fallback_result.user_message}", 
                "error"
            )
            if fallback_result.alternative_action:
                print_status_message(
                    f"Suggested action: {fallback_result.alternative_action}", 
                    "info"
                )
            print_status_message("Continuing with next request...", "warning")
            print()
            
            # Log error
            if self.conversation_logger:
                self.conversation_logger.add_status_message(
                    f"Error processing response: {fallback_result.user_message}",
                    "error"
                )
        
        # Log assistant response
        if self.conversation_logger and assistant_response_parts:
            full_response = "\n".join(assistant_response_parts)
            self.conversation_logger.add_assistant_message(full_response)
        
        # Record timing
        if self.stats:
            response_time = self.stats.end_request()
        
        return response_time
    
    async def _process_part(self, event: Any, part: Any) -> Optional[ProcessedEvent]:
        """Process a single part using appropriate handler."""
        for handler in self.handlers:
            if handler.can_handle(event, part):
                processed = await handler.handle(event, part)
                
                # Log if needed
                if processed.should_log and self.conversation_logger:
                    self._log_processed_event(processed)
                
                return processed
        
        return None
    
    async def _process_event_metadata(self, event: Any):
        """Process event-level metadata."""
        # Check handlers that work on the event level (not parts)
        for handler in self.handlers:
            if handler.can_handle(event, None):
                if handler.get_event_type() in [EventType.GROUNDING_METADATA, EventType.URL_CONTEXT]:
                    processed = await handler.handle(event, None)
                    
                    if processed.should_log and self.conversation_logger:
                        self._log_processed_event(processed)
    
    def _log_processed_event(self, processed: ProcessedEvent):
        """Log processed event based on type."""
        if not self.conversation_logger:
            return
        
        if processed.event_type == EventType.FUNCTION_CALL:
            # Function calls are logged with responses
            pass
        elif processed.event_type == EventType.FUNCTION_RESPONSE:
            content = processed.content
            if content.get('call_info'):
                self.conversation_logger.add_tool_call(
                    content['call_info']['name'],
                    content['call_info']['args'],
                    content['response']
                )
        elif processed.event_type in [EventType.GROUNDING_METADATA, EventType.URL_CONTEXT]:
            self.conversation_logger.add_metadata({
                "type": processed.event_type.value,
                **processed.metadata
            })


# Factory function for backward compatibility
async def process_events(events_async, error_recovery_system: ErrorRecoverySystem, 
                         stats: ConversationStats = None, conversation_logger = None, 
                         loading_indicator = None):
    """Legacy interface for event processing."""
    processor = EventProcessor(error_recovery_system, conversation_logger, stats)
    return await processor.process_events(events_async, loading_indicator)