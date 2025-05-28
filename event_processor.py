"""
Event processing module for MCP Agent system.
Contains all event handling and response processing logic.
"""

from mcp_agent_utils import (
    COLOR_GREEN, COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA, COLOR_RESET,
    COLOR_BLUE, COLOR_DIM, SYMBOL_SUCCESS, SYMBOL_WARNING, SYMBOL_THINKING,
    SYMBOL_TOOL, SYMBOL_SEARCH, SYMBOL_INFO, pretty_print_json_string,
    print_section_header, print_status_message, format_tool_response,
    ConversationStats
)
from error_recovery_system import ErrorRecoverySystem, create_failure_context


async def process_events(events_async, error_recovery_system: ErrorRecoverySystem, stats: ConversationStats = None):
    """Process events from the agent response with comprehensive error handling."""
    response_time = None
    try:
        async for event in events_async:
            has_printed_content = False
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print_section_header("Agent Response", width=50)
                        # Print each line of multi-line text with color
                        for line in part.text.splitlines():
                            print(f"{COLOR_GREEN}{line}{COLOR_RESET}")
                        print() # Add blank line for separation
                        has_printed_content = True
                    if part.function_call:
                        print_section_header(f"Tool Call: {part.function_call.name}", width=50)
                        pretty_print_json_string(part.function_call.args, COLOR_YELLOW)
                        print() # Add blank line for separation
                        has_printed_content = True
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
                        if isinstance(actual_response_data, dict) and 'content' in actual_response_data:
                            format_tool_response(tool_name_for_response, actual_response_data['content'])
                        else:
                            format_tool_response(tool_name_for_response, actual_response_data)
                        has_printed_content = True
            
            # Display grounding metadata if available
            if hasattr(event, 'candidates') and event.candidates:
                for candidate in event.candidates:
                    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                        grounding = candidate.grounding_metadata
                        if hasattr(grounding, 'web_search_queries') and grounding.web_search_queries:
                            print_section_header("Web Search Queries", width=50)
                            for query in grounding.web_search_queries:
                                print(f"{COLOR_CYAN}  {SYMBOL_SEARCH} {query}{COLOR_RESET}")
                            print() # Add blank line for separation
                            has_printed_content = True
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
                            print() # Add blank line for separation
                            has_printed_content = True
                        
                        # Display URL Context Metadata if available
                        if hasattr(candidate, 'url_context_metadata') and candidate.url_context_metadata:
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
                        if hasattr(grounding, 'search_entry_point') and \
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
            
            if not has_printed_content: # If no specific part was printed above
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
    
    # End timing and return response time
    if stats:
        response_time = stats.end_request()
    return response_time