"""
Event processing module for MCP Agent system.
Contains all event handling and response processing logic.
"""

from ..utils.mcp_agent_utils import (
    COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA, COLOR_RESET,
    COLOR_BLUE, COLOR_DIM, SYMBOL_SUCCESS, SYMBOL_WARNING, SYMBOL_THINKING,
    SYMBOL_TOOL, SYMBOL_SEARCH, SYMBOL_INFO, pretty_print_json_string,
    print_section_header, print_status_message, format_tool_response,
    ConversationStats
)
from ..core.error_recovery_system import ErrorRecoverySystem, create_failure_context
from ..utils.telegram_formatter import markdown_to_plain_text
from ..utils.compact_formatter import format_compact
from ..ui.shell_ui import ShellUI


async def process_events(events_async, error_recovery_system: ErrorRecoverySystem, stats: ConversationStats = None, conversation_logger = None, loading_indicator = None, shell_mode: bool = False):
    """Process events from the agent response with comprehensive error handling."""
    response_time = None
    assistant_response_parts = []
    first_event = True
    tools_used = set()  # Track unique tools used
    try:
        async for event in events_async:
            # Stop loading indicator on first event to prevent display interference
            if first_event:
                first_event = False
                if loading_indicator:
                    loading_indicator.stop()
                if shell_mode:
                    # Clear the "Working..." line
                    print("\r" + " " * 50 + "\r", end="")
                    print()
            has_printed_content = False
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        if not shell_mode:
                            print_section_header("Agent Response", width=50)
                        else:
                            ShellUI.format_response_header("Response")
                        # Remove markdown formatting for better CLI readability
                        clean_text = markdown_to_plain_text(part.text)
                        # Apply compact formatting for better readability
                        formatted_text = format_compact(clean_text)
                        # Print the formatted text with shell UI formatting if in shell mode
                        if shell_mode:
                            print(ShellUI.format_response(formatted_text))
                        else:
                            print(formatted_text)
                        print() # Add blank line for separation
                        has_printed_content = True
                        assistant_response_parts.append(part.text)
                    if part.function_call:
                        # Track tool usage for shell mode
                        tools_used.add(part.function_call.name)
                        
                        if not shell_mode:
                            print_section_header(f"Tool Call: {part.function_call.name}", width=50)
                            pretty_print_json_string(part.function_call.args, COLOR_YELLOW)
                            print() # Add blank line for separation
                        has_printed_content = True
                        
                        # Log tool call if logger available
                        if conversation_logger:
                            import json
                            try:
                                args_dict = json.loads(part.function_call.args)
                            except:
                                args_dict = {"raw_args": part.function_call.args}
                            # Store tool call info for later when we get the response
                            if not hasattr(process_events, 'pending_tool_call'):
                                process_events.pending_tool_call = {}
                            process_events.pending_tool_call = {
                                "name": part.function_call.name,
                                "args": args_dict
                            }
                    if part.function_response:
                        # Assuming function_response.response might contain a 'name' if it's structured,
                        # otherwise, it might be a simple string or dict.
                        # For ADK, function_response.name refers to the tool name.
                        tool_name_for_response = "UnknownTool" # Default
                        if hasattr(part.function_response, 'name') and part.function_response.name:
                            tool_name_for_response = part.function_response.name

                        # The actual response content is in part.function_response.response
                        # This 'response' field itself can be a dict containing 'content' or other structured data.
                        actual_response_data = part.function_response.response
                        if not shell_mode:
                            if isinstance(actual_response_data, dict) and 'content' in actual_response_data:
                                format_tool_response(tool_name_for_response, actual_response_data['content'])
                                response_str = str(actual_response_data['content'])
                            else:
                                format_tool_response(tool_name_for_response, actual_response_data)
                                response_str = str(actual_response_data)
                        else:
                            if isinstance(actual_response_data, dict) and 'content' in actual_response_data:
                                response_str = str(actual_response_data['content'])
                            else:
                                response_str = str(actual_response_data)
                        has_printed_content = True
                        
                        # Log tool response if logger available
                        if conversation_logger and hasattr(process_events, 'pending_tool_call'):
                            conversation_logger.add_tool_call(
                                process_events.pending_tool_call["name"],
                                process_events.pending_tool_call["args"],
                                response_str
                            )
                            delattr(process_events, 'pending_tool_call')
            
            # Display grounding metadata if available
            if hasattr(event, 'candidates') and event.candidates:
                for candidate in event.candidates:
                    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                        grounding = candidate.grounding_metadata
                        if hasattr(grounding, 'web_search_queries') and grounding.web_search_queries:
                            if not shell_mode:
                                print_section_header("Web Search Queries", width=50)
                                for query in grounding.web_search_queries:
                                    print(f"{COLOR_CYAN}  {SYMBOL_SEARCH} {query}{COLOR_RESET}")
                                print() # Add blank line for separation
                            has_printed_content = True
                            
                            # Log search queries as metadata
                            if conversation_logger:
                                conversation_logger.add_metadata({
                                    "type": "web_search_queries",
                                    "queries": list(grounding.web_search_queries)
                                })
                        if hasattr(grounding, 'grounding_chunks') and grounding.grounding_chunks:
                            if not shell_mode:
                                print_section_header("Grounding Sources", width=50)
                            if not shell_mode:
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
                                print() # Add blank line for separation
                            has_printed_content = True
                            
                            # Log grounding sources as metadata  
                            if conversation_logger:
                                sources = []
                                for chunk in grounding.grounding_chunks:
                                    if hasattr(chunk, 'web'):
                                        sources.append({
                                            "title": chunk.web.title if hasattr(chunk.web, 'title') else "N/A",
                                            "uri": chunk.web.uri if hasattr(chunk.web, 'uri') else "N/A"
                                        })
                                conversation_logger.add_metadata({
                                    "type": "grounding_sources",
                                    "sources": sources
                                })
                        
                        # Display URL Context Metadata if available
                        if not shell_mode and hasattr(candidate, 'url_context_metadata') and candidate.url_context_metadata:
                            url_meta_data = candidate.url_context_metadata
                            if hasattr(url_meta_data, 'url_metadata') and url_meta_data.url_metadata:
                                print_section_header("URL Context Metadata", width=50)
                                for i, meta_item in enumerate(url_meta_data.url_metadata):
                                    retrieved_url = meta_item.retrieved_url if hasattr(meta_item, 'retrieved_url') else "N/A"
                                    status = meta_item.url_retrieval_status if hasattr(meta_item, 'url_retrieval_status') else "N/A"
                                    # Ensure status is converted to string if it's an enum-like object for printing
                                    status_str = str(status) if status != "N/A" else "N/A"
                                    status_symbol = SYMBOL_SUCCESS if "success" in status_str.lower() else SYMBOL_WARNING
                                    print(f"{COLOR_BLUE}  {status_symbol} URL {i+1}: {retrieved_url[:60]}{'...' if len(retrieved_url) > 60 else ''}{COLOR_RESET}")
                                    print(f"{COLOR_DIM}    Status: {status_str}{COLOR_RESET}")
                                print()
                                has_printed_content = True

                        # Display rendered search suggestions HTML
                        if not shell_mode and hasattr(grounding, 'search_entry_point') and \
                           hasattr(grounding.search_entry_point, 'rendered_content') and \
                           grounding.search_entry_point.rendered_content:
                            print(f"{COLOR_CYAN}--- Rendered Search Suggestions (HTML) ---{COLOR_RESET}")
                            # webSearchQueries (printed above) are the text of these suggestions.
                            # This rendered_content is HTML for rich display in a UI.
                            print(f"{COLOR_CYAN}Raw HTML for rich display (first 500 chars):{COLOR_RESET}")
                            html_content = grounding.search_entry_point.rendered_content
                            # Ensure html_content is a string before slicing
                            html_content_str = str(html_content)
                            print(f"{COLOR_MAGENTA}{html_content_str[:500]}{'...' if len(html_content_str) > 500 else ''}{COLOR_RESET}")
                            print() # Add blank line for separation
                            has_printed_content = True
            
            if not has_printed_content and not shell_mode: # If no specific part was printed above
                print(f"{COLOR_MAGENTA}--- Event Information ---{COLOR_RESET}")
                # Print event information without attempting JSON formatting
                try:
                    event_str = str(event)
                    print(f"{COLOR_MAGENTA}{event_str}{COLOR_RESET}")
                except Exception as e:
                    print(f"{COLOR_MAGENTA}Error displaying event: {e}{COLOR_RESET}")
                print() # Add blank line for separation
    except Exception as e:
        # Enhanced error handling with recovery suggestions
        context = create_failure_context(e, tool_name="event_processor", user_intent="process_agent_response")
        fallback_result = await error_recovery_system.handle_failure(context)
        
        print_status_message(f"Error processing response: {fallback_result.user_message}", "error")
        if fallback_result.alternative_action:
            print_status_message(f"Suggested action: {fallback_result.alternative_action}", "info")
        print_status_message("Continuing with next request...", "warning")
        print() # Add blank line for separation
        
        # Log error if logger available
        if conversation_logger:
            conversation_logger.add_status_message(
                f"Error processing response: {fallback_result.user_message}",
                "error"
            )
    
    # Show tools used in shell mode
    if shell_mode and tools_used:
        tools_list = ", ".join(sorted(tools_used))
        print(f"{COLOR_DIM}Used: {COLOR_YELLOW}{tools_list}{COLOR_RESET}")
    
    # Log assistant response if we collected any text
    if conversation_logger and assistant_response_parts:
        full_response = "\n".join(assistant_response_parts)
        conversation_logger.add_assistant_message(full_response)
    
    # End timing and return response time
    if stats:
        response_time = stats.end_request()
    return response_time