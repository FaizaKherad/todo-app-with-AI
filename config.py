"""
Configuration settings for the Core Todo Engine with Conversational AI
"""
import os

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.getenv("LOG_FILE", "todo_app.log")  # Set to None to disable file logging

# Application settings
MAX_TITLE_LENGTH = 255  # Updated from Phase II (was 100)
MAX_DESCRIPTION_LENGTH = 1000  # Updated from Phase II (was 500)

# Storage settings (for future phases)
STORAGE_TYPE = "file"  # Updated from Phase II (was "in-memory")

# AI Assistant settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # API key for OpenAI integration
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")  # Model to use for AI assistant
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))  # Creativity setting for AI responses

# MCP Integration settings
MCP_ENABLED = os.getenv("MCP_ENABLED", "true").lower() == "true"  # Enable MCP tools