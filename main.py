#!/usr/bin/env python3
"""
Main entry point for the Google ADK Agent.
"""

import sys
from src.core.mcp_agent import async_main
import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nAgent interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("The agent will restart automatically. Please try your request again.")