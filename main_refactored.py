#!/usr/bin/env python3
"""
Main entry point for the refactored Google ADK Agent.
"""

import sys
import asyncio
from src.core.mcp_agent_refactored import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("The agent will restart automatically. Please try your request again.")