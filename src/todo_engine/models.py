"""
Task data model for the Core Todo Engine
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import re


@dataclass
class Task:
    """
    Represents a single todo item with all required fields.

    Attributes:
        id: Unique identifier (UUID v4)
        title: Short task title (1-255 characters)
        description: Optional task details (0-1000 characters)
        completed: Completion status
        created_at: ISO 8601 timestamp when task was created
        updated_at: ISO 8601 timestamp when task was last updated
    """
    id: str
    title: str
    description: Optional[str] = ""
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        """Validate the task after initialization."""
        # Set timestamps if not provided
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()

        # Validate title
        if not self.title or len(self.title) == 0:
            raise ValueError("Title cannot be empty")
        if len(self.title) > 255:
            raise ValueError("Title cannot exceed 255 characters")

        # Validate description
        if self.description and len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Validate UUID format
        try:
            UUID(self.id)
        except ValueError:
            raise ValueError("ID must be a valid UUID")


def create_task(title: str, description: Optional[str] = "") -> Task:
    """
    Create a new task with the given title and optional description.

    Args:
        title: Task title (1-255 characters)
        description: Optional task description (0-1000 characters)

    Returns:
        Task: A new Task instance

    Raises:
        ValueError: If title or description validation fails
    """
    if not title or len(title) == 0:
        raise ValueError("Title cannot be empty")
    if len(title) > 255:
        raise ValueError("Title cannot exceed 255 characters")
    if description and len(description) > 1000:
        raise ValueError("Description cannot exceed 1000 characters")

    task_id = str(uuid4())
    now = datetime.now().isoformat()

    return Task(
        id=task_id,
        title=title,
        description=description,
        completed=False,  # Default to False
        created_at=now,
        updated_at=now
    )


def update_task(task: Task, title: Optional[str] = None, description: Optional[str] = None) -> Task:
    """
    Update a task with new title and/or description.

    Args:
        task: The task to update
        title: New title (1-255 characters, optional)
        description: New description (0-1000 characters, optional)

    Returns:
        Task: The updated Task instance

    Raises:
        ValueError: If title or description validation fails
    """
    if title is not None:
        if not title or len(title) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        task.title = title

    if description is not None:
        if len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        task.description = description

    task.updated_at = datetime.now().isoformat()
    return task


def toggle_task_completion(task: Task) -> Task:
    """
    Toggle the completion status of a task.
    
    Args:
        task: The task to toggle
        
    Returns:
        Task: The task with toggled completion status
    """
    task.completed = not task.completed
    task.updated_at = datetime.now().isoformat()
    return task