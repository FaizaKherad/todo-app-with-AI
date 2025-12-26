"""
Logging utilities for the Core Todo Engine
"""
import logging
import sys
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """Enumeration for log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def setup_logger(name: str = "todo_engine",
                log_file: str = "todo_app.log",
                level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with file handler only (no console output to avoid interfering with JSON output).

    Args:
        name: Name of the logger
        log_file: File to write logs to (set to None to disable file logging)
        level: Minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Set the logging level
    logger.setLevel(getattr(logging, level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create file handler if log_file is specified
    # We're not adding a console handler to avoid interfering with JSON output
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def log_user_action(logger: logging.Logger, action: str, details: str = ""):
    """
    Log a user action.
    
    Args:
        logger: The logger instance
        action: The action performed (e.g., "add_task", "delete_task")
        details: Additional details about the action
    """
    logger.info(f"USER_ACTION: {action} - {details}")


def log_system_event(logger: logging.Logger, event: str, details: str = ""):
    """
    Log a system event.
    
    Args:
        logger: The logger instance
        event: The event that occurred (e.g., "startup", "shutdown", "error")
        details: Additional details about the event
    """
    logger.info(f"SYSTEM_EVENT: {event} - {details}")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log an error with context.
    
    Args:
        logger: The logger instance
        error: The exception that occurred
        context: Context about where the error occurred
    """
    logger.error(f"ERROR in {context}: {str(error)}", exc_info=True)