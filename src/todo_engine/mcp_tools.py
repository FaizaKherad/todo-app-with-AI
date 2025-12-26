"""
MCP Tools Module for Conversational AI Interface
Implements the required MCP tools for task management operations
"""
import os
from typing import Dict, Any, List
from .models import create_task, update_task, toggle_task_completion
from .storage import storage
from .persistence import FilePersistence


class MCPTaskTools:
    """
    Implementation of MCP tools for task management operations.
    Each method corresponds to a required MCP tool as specified in the feature requirements.
    """
    
    def __init__(self):
        """
        Initialize the MCP tools with access to storage and persistence layers.
        """
        self.storage = storage
        self.persistence = FilePersistence()

        # Get MCP server URL from environment variable (for internal cluster communication)
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", None)

        # If MCP server URL is set, we might be in a distributed architecture
        # For Phase IV, we'll continue using the local implementation but note the setting
        if self.mcp_server_url:
            print(f"MCP Server configured at: {self.mcp_server_url}")
            # In a full implementation, we would connect to the external MCP server
            # For this phase, we'll continue using local implementation but acknowledge the setting
    
    def add_task(self, title: str, description: str = "") -> Dict[str, Any]:
        """
        MCP tool for adding a new task.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            
        Returns:
            Dictionary containing the created task details
        """
        # Validate inputs according to Phase II requirements
        if not title or len(title) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 255:
            raise ValueError("Title cannot exceed 255 characters")
        if description and len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        
        # Create task using Phase II logic
        task = create_task(title, description)
        self.storage.add_task(task)
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
    
    def view_tasks(self) -> List[Dict[str, Any]]:
        """
        MCP tool for viewing all tasks.
        
        Returns:
            List of all tasks as dictionaries
        """
        tasks = self.storage.get_all_tasks()
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            for task in tasks
        ]
    
    def update_task(self, task_id: str, title: str = None, description: str = None) -> Dict[str, Any]:
        """
        MCP tool for updating an existing task.
        
        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            
        Returns:
            Dictionary containing the updated task details
        """
        # Validate task_id exists
        task = self.storage.get_task(task_id)
        if not task:
            raise ValueError(f"TASK_NOT_FOUND: Task with ID {task_id} does not exist")
        
        # Validate inputs according to Phase II requirements
        if title is not None:
            if not title or len(title) == 0:
                raise ValueError("Title cannot be empty")
            if len(title) > 255:
                raise ValueError("Title cannot exceed 255 characters")
        
        if description is not None and len(description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        
        # Update task using Phase II logic
        updated_task = update_task(task, title, description)
        self.storage.update_task(task_id, updated_task)
        
        return {
            "id": updated_task.id,
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed,
            "created_at": updated_task.created_at,
            "updated_at": updated_task.updated_at
        }
    
    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """
        MCP tool for deleting a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            Dictionary confirming the deletion
        """
        # Validate task_id exists
        task = self.storage.get_task(task_id)
        if not task:
            raise ValueError(f"TASK_NOT_FOUND: Task with ID {task_id} does not exist")
        
        # Delete task using Phase II logic
        success = self.storage.delete_task(task_id)
        if not success:
            raise ValueError(f"TASK_NOT_FOUND: Task with ID {task_id} does not exist")
        
        return {
            "message": "Task deleted successfully",
            "deleted_task_id": task_id
        }
    
    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """
        MCP tool for toggling task completion status.
        
        Args:
            task_id: ID of the task to update completion status
            
        Returns:
            Dictionary containing the updated task details
        """
        # Validate task_id exists
        task = self.storage.get_task(task_id)
        if not task:
            raise ValueError(f"TASK_NOT_FOUND: Task with ID {task_id} does not exist")
        
        # Toggle completion using Phase II logic
        updated_task = toggle_task_completion(task)
        self.storage.update_task(task_id, updated_task)
        
        return {
            "id": updated_task.id,
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed,
            "created_at": updated_task.created_at,
            "updated_at": updated_task.updated_at
        }


# Global instance of MCP tools
mcp_tools = MCPTaskTools()