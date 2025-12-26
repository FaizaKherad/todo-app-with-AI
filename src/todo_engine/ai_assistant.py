"""
AI Assistant Module for Conversational Todo Interface
Implements intent recognition, parameter extraction, and command routing
"""
import json
import re
from typing import Dict, Any, List, Tuple
from .mcp_tools import MCPTaskTools


class TodoAIAssistant:
    """
    AI assistant for interpreting natural language commands and routing them to appropriate functions.
    Acts as an intent interpreter, command router, and response formatter as specified in the feature requirements.
    """

    def __init__(self):
        """
        Initialize the AI assistant with MCP tools access.
        """
        self.mcp_tools = MCPTaskTools()

    def process_command(self, user_input: str) -> Dict[str, Any]:
        """
        Process a natural language command from the user.

        Args:
            user_input: Natural language command from the user

        Returns:
            Dictionary containing the result of the command execution
        """
        try:
            # Identify the intent and extract parameters from user input
            intent, params = self._parse_intent_and_params(user_input)

            # Route the command to the appropriate MCP tool based on the intent
            if intent == "create_task":
                return self._handle_create_task(params)
            elif intent == "view_tasks":
                return self._handle_view_tasks(params)
            elif intent == "update_task":
                return self._handle_update_task(params)
            elif intent == "delete_task":
                return self._handle_delete_task(params)
            elif intent == "complete_task":
                return self._handle_complete_task(params)
            else:
                return {
                    "status": "error", 
                    "error": {
                        "error_code": "UNKNOWN_INTENT", 
                        "message": f"Could not understand the intent: {intent}"
                    }
                }

        except Exception as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "PROCESSING_ERROR", 
                    "message": str(e)
                }
            }

    def _parse_intent_and_params(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Use rule-based parsing to identify intent and extract parameters from user input.

        Args:
            user_input: Natural language command from the user

        Returns:
            Tuple of (intent, parameters)
        """
        user_input_lower = user_input.lower().strip()

        # Intent patterns
        create_patterns = [
            r'(add|create|make|new)\s+(a\s+)?(task|todo|to-do)\s+(to|called|named)?\s*(.*)',
            r'(add|create|make|new)\s+(a\s+)?(task|todo|to-do):\s*(.*)',
            r'(add|create|make|new)\s+(.*)'
        ]

        view_patterns = [
            r'(show|display|list|view|see|what)\s+(are|is|do)\s+(my|the)\s*(tasks|todos|to-dos|things|items|needed|todo)',
            r'(show|display|list|view|see|what)\s+(are|is|do)\s+(i|I)\s*(need|have|to\s+do|to\s+complete)',
            r'(my|the)\s*(tasks|todos|to-dos)'
        ]

        update_patterns = [
            r'(update|change|rename|edit|modify)\s+(the\s+)?(.*)',
            r'(update|change|rename|edit|modify)\s+(.*)'
        ]

        delete_patterns = [
            r'(delete|remove|erase|eliminate)\s+(the\s+)?(.*)',
            r'(delete|remove|erase|eliminate)\s+(.*)'
        ]

        complete_patterns = [
            r'(mark|complete|finish|done|toggle|accomplish)\s+(the\s+)?(.*)',
            r'(mark|complete|finish|done|toggle|accomplish)\s+(.*)'
        ]

        user_input_lower = user_input.lower().strip()

        # Intent patterns
        create_patterns = [
            r'(add|create|make|new)\s+(a\s+)?(task|todo|to-do)\s+(to|called|named)?\s*(.*)',
            r'(add|create|make|new)\s+(a\s+)?(task|todo|to-do):\s*(.*)',
            r'(add|create|make|new)\s+(.*)'
        ]

        view_patterns = [
            r'(show|display|list|view|see|what)\s+(are|is|do)\s+(my|the)\s*(tasks|todos|to-dos|things|items|needed|todo)',
            r'(show|display|list|view|see|what)\s+(are|is|do)\s+(i|I)\s*(need|have|to\s+do|to\s+complete)',
            r'(my|the)\s*(tasks|todos|to-dos)'
        ]

        update_patterns = [
            r'(update|change|rename|edit|modify)\s+(the\s+)?(.*)',
            r'(update|change|rename|edit|modify)\s+(.*)'
        ]

        delete_patterns = [
            r'(delete|remove|erase|eliminate)\s+(the\s+)?(.*)',
            r'(delete|remove|erase|eliminate)\s+(.*)'
        ]

        complete_patterns = [
            r'(mark|complete|finish|done|toggle|accomplish)\s+(the\s+)?(.*)',
            r'(mark|complete|finish|done|toggle|accomplish)\s+(.*)'
        ]

        # Check for create task intent
        for pattern in create_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                groups = match.groups()
                # Extract the task information part
                task_info = groups[-1].strip()  # Last group usually contains the task info

                # Look for description patterns within the task info
                title = task_info
                description = ""

                # Try to extract description if mentioned
                desc_match = re.search(r'(with\s+description|description\s+is|desc\s+is):\s*(.*)', task_info, re.IGNORECASE)
                if desc_match:
                    title = task_info.split(desc_match.group(0))[0].strip()
                    description = desc_match.group(1).strip()
                    # Clean up the description pattern from title
                    title = re.sub(r'\s*(with\s+description|description\s+is|desc\s+is):\s*.*$', '', title, flags=re.IGNORECASE).strip()

                return "create_task", {"title": title, "description": description}

        # Check for view tasks intent
        for pattern in view_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                return "view_tasks", {}

        # Check for update task intent
        for pattern in update_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                extracted_part = match.groups()[-1].strip()
                # For now, simplified - in practice, you'd need more sophisticated parsing
                return "update_task", {"task_info": extracted_part}

        # Check for delete task intent
        for pattern in delete_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                extracted_part = match.groups()[-1].strip()
                return "delete_task", {"task_info": extracted_part}

        # Check for complete task intent
        for pattern in complete_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                extracted_part = match.groups()[-1].strip()
                return "complete_task", {"task_info": extracted_part}

        # If no intent matched, return unknown
        return "unknown", {}

    def _handle_create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle create task command.

        Args:
            params: Parameters extracted from user input

        Returns:
            Result of the create task operation
        """
        title = params.get("title", "").strip()
        description = params.get("description", "").strip()

        if not title:
            return {
                "status": "error",
                "error": {
                    "error_code": "MISSING_TITLE", 
                    "message": "Title is required for creating a task"
                }
            }

        try:
            result = self.mcp_tools.add_task(title, description)
            return {
                "status": "success",
                "data": {
                    "message": f"[ADDED] Task '{result['title']}' has been added.",
                    "task": result
                }
            }
        except ValueError as e:
            return {
                "status": "error", 
                "error": {
                    "error_code": "VALIDATION_ERROR", 
                    "message": str(e)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "CREATE_TASK_ERROR", 
                    "message": str(e)
                }
            }

    def _handle_view_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle view tasks command.

        Args:
            params: Parameters extracted from user input

        Returns:
            Result of the view tasks operation
        """
        try:
            tasks = self.mcp_tools.view_tasks()

            if not tasks:
                return {
                    "status": "success",
                    "data": {
                        "message": "[TASKS] You have no tasks in your list.",
                        "tasks": tasks
                    }
                }

            return {
                "status": "success",
                "data": {
                    "message": f"[TASKS] You have {len(tasks)} task(s) in your list.",
                    "tasks": tasks
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "VIEW_TASKS_ERROR", 
                    "message": str(e)
                }
            }

    def _handle_update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle update task command.

        Args:
            params: Parameters extracted from user input

        Returns:
            Result of the update task operation
        """
        task_info = params.get("task_info", "").strip()

        # Find task by partial title match (case insensitive)
        all_tasks = self.mcp_tools.view_tasks()
        matching_tasks = [
            task for task in all_tasks
            if task_info.lower() in task["title"].lower()
        ]

        if not matching_tasks:
            return {
                "status": "error",
                "error": {
                    "error_code": "TASK_NOT_FOUND",
                    "message": f"I couldn't find a task with title containing '{task_info}'."
                }
            }

        if len(matching_tasks) > 1:
            # Ask for clarification if multiple tasks match
            task_titles = [task["title"] for task in matching_tasks]
            return {
                "status": "error",
                "error": {
                    "error_code": "AMBIGUOUS_TASK",
                    "message": f"Multiple tasks match '{task_info}': {', '.join(task_titles)}. Please be more specific."
                }
            }

        # For now, update the first matching task
        task_id = matching_tasks[0]["id"]

        # Extract update parameters from the original user input
        # This would need more sophisticated parsing in a real implementation
        title = params.get("title")
        description = params.get("description")

        try:
            result = self.mcp_tools.update_task(task_id, title, description)
            return {
                "status": "success",
                "data": {
                    "message": f"[UPDATED] Task '{result['title']}' has been updated.",
                    "task": result
                }
            }
        except ValueError as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "VALIDATION_ERROR", 
                    "message": str(e)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "UPDATE_TASK_ERROR", 
                    "message": str(e)
                }
            }

    def _handle_delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle delete task command.

        Args:
            params: Parameters extracted from user input

        Returns:
            Result of the delete task operation
        """
        task_info = params.get("task_info", "").strip()

        # Find task by partial title match
        all_tasks = self.mcp_tools.view_tasks()
        matching_tasks = [
            task for task in all_tasks
            if task_info.lower() in task["title"].lower()
        ]

        if not matching_tasks:
            return {
                "status": "error",
                "error": {
                    "error_code": "TASK_NOT_FOUND",
                    "message": f"I couldn't find a task with title containing '{task_info}'."
                }
            }

        if len(matching_tasks) > 1:
            # Ask for clarification if multiple tasks match
            task_titles = [task["title"] for task in matching_tasks]
            return {
                "status": "error",
                "error": {
                    "error_code": "AMBIGUOUS_TASK",
                    "message": f"Multiple tasks match '{task_info}': {', '.join(task_titles)}. Please be more specific."
                }
            }

        # Delete the first matching task
        task_id = matching_tasks[0]["id"]

        try:
            result = self.mcp_tools.delete_task(task_id)
            return {
                "status": "success",
                "data": {
                    "message": f"[DELETED] Task has been deleted.",
                    "result": result
                }
            }
        except ValueError as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "VALIDATION_ERROR", 
                    "message": str(e)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "DELETE_TASK_ERROR", 
                    "message": str(e)
                }
            }

    def _handle_complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle complete task command.

        Args:
            params: Parameters extracted from user input

        Returns:
            Result of the complete task operation
        """
        task_info = params.get("task_info", "").strip()

        # Find task by partial title match
        all_tasks = self.mcp_tools.view_tasks()
        matching_tasks = [
            task for task in all_tasks
            if task_info.lower() in task["title"].lower()
        ]

        if not matching_tasks:
            return {
                "status": "error",
                "error": {
                    "error_code": "TASK_NOT_FOUND",
                    "message": f"I couldn't find a task with title containing '{task_info}'."
                }
            }

        if len(matching_tasks) > 1:
            # Ask for clarification if multiple tasks match
            task_titles = [task["title"] for task in matching_tasks]
            return {
                "status": "error",
                "error": {
                    "error_code": "AMBIGUOUS_TASK",
                    "message": f"Multiple tasks match '{task_info}': {', '.join(task_titles)}. Please be more specific."
                }
            }

        # Complete the first matching task
        task_id = matching_tasks[0]["id"]

        try:
            result = self.mcp_tools.complete_task(task_id)
            status = "completed" if result["completed"] else "marked incomplete"
            return {
                "status": "success",
                "data": {
                    "message": f"[COMPLETED] Task '{result['title']}' has been {status}.",
                    "task": result
                }
            }
        except ValueError as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "VALIDATION_ERROR", 
                    "message": str(e)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": {
                    "error_code": "COMPLETE_TASK_ERROR", 
                    "message": str(e)
                }
            }


# Global instance of the AI assistant
ai_assistant = TodoAIAssistant()