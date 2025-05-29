"""
Token counting and context window management for Google ADK agents.
"""
import tiktoken
from typing import List, Dict, Any
from google.genai import types

class TokenManager:
    def __init__(self, model_name: str = "gpt-4", max_context_tokens: int = 120000):
        """
        Initialize token manager.
        
        Args:
            model_name: Model name for tiktoken encoding (fallback to gpt-4 for Gemini)
            max_context_tokens: Maximum context window size
        """
        # Use gpt-4 encoding as fallback for Gemini models since tiktoken doesn't support them directly
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4")
        except:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        self.max_context_tokens = max_context_tokens
        self.safety_margin = 2000  # Reserve tokens for response
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def count_content_tokens(self, content: types.Content) -> int:
        """Count tokens in a Content object."""
        total_tokens = 0
        if content.parts:
            for part in content.parts:
                if part.text:
                    total_tokens += self.count_tokens(part.text)
                # Add small overhead for function calls/responses
                elif part.function_call or part.function_response:
                    total_tokens += 100
        return total_tokens
    
    def should_truncate_history(self, conversation_history: List[types.Content]) -> bool:
        """Check if conversation history exceeds safe token limit."""
        total_tokens = sum(self.count_content_tokens(content) for content in conversation_history)
        return total_tokens > (self.max_context_tokens - self.safety_margin)
    
    def truncate_conversation_history(self, conversation_history: List[types.Content]) -> List[types.Content]:
        """
        Truncate conversation history to fit within token limits.
        Keeps the first message (system prompt) and most recent messages.
        """
        if not conversation_history:
            return conversation_history
            
        if not self.should_truncate_history(conversation_history):
            return conversation_history
        
        # Always keep the first message (usually system prompt)
        truncated = [conversation_history[0]] if conversation_history else []
        remaining_tokens = self.max_context_tokens - self.safety_margin
        remaining_tokens -= self.count_content_tokens(conversation_history[0])
        
        # Add messages from the end, working backwards
        for content in reversed(conversation_history[1:]):
            content_tokens = self.count_content_tokens(content)
            if content_tokens <= remaining_tokens:
                truncated.insert(1, content)  # Insert after system prompt
                remaining_tokens -= content_tokens
            else:
                break
                
        return truncated
    
    def split_large_message(self, text: str, max_chunk_tokens: int = None) -> List[str]:
        """
        Split a large text message into smaller chunks.
        
        Args:
            text: Text to split
            max_chunk_tokens: Maximum tokens per chunk (defaults to safe limit)
        """
        if max_chunk_tokens is None:
            max_chunk_tokens = self.max_context_tokens - self.safety_margin
            
        if self.count_tokens(text) <= max_chunk_tokens:
            return [text]
        
        # Split by sentences/paragraphs first, then by words if needed
        chunks = []
        current_chunk = ""
        
        # Try splitting by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            paragraph_tokens = self.count_tokens(paragraph)
            current_tokens = self.count_tokens(current_chunk)
            
            if current_tokens + paragraph_tokens <= max_chunk_tokens:
                current_chunk += ("\n\n" + paragraph) if current_chunk else paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                
                # If single paragraph is too large, split by sentences
                if paragraph_tokens > max_chunk_tokens:
                    sentences = paragraph.split('. ')
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if not sentence:
                            continue
                        if not sentence.endswith('.'):
                            sentence += '.'
                            
                        sentence_tokens = self.count_tokens(sentence)
                        current_tokens = self.count_tokens(current_chunk)
                        
                        if current_tokens + sentence_tokens <= max_chunk_tokens:
                            current_chunk += (" " + sentence) if current_chunk else sentence
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            current_chunk = sentence
                else:
                    current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks