"""
Conversational AI Skill for Qwen
Handles natural language processing for todo management as specified in the constitution
"""

import re
from typing import Dict, List, Optional
from .todo_management import add_task, delete_task, update_task, view_tasks, mark_complete

class TodoAIInterpreter:
    """
    Interprets natural language commands for todo management
    Following the AI Chatbot Rules from Constitution section 6
    """
    
    def __init__(self):
        self.commands = {
            'add': [
                r'add.*task.*"([^"]+)"',
                r'add.*task.*\'([^\']+)\'',
                r'create.*task.*"([^"]+)"',
                r'create.*task.*\'([^\']+)\'',
                r'new.*task.*"([^"]+)"',
                r'new.*task.*\'([^\']+)\'',
                r'"([^"]+)"',
                r"'([^']+)'"
            ],
            'delete': [
                r'delete.*task.*(\d+)',
                r'remove.*task.*(\d+)',
                r'delete.*#(\d+)',
                r'remove.*#(\d+)'
            ],
            'update': [
                r'update.*task.*(\d+).*to.*"([^"]+)"',
                r'change.*task.*(\d+).*to.*"([^"]+)"',
                r'modify.*task.*(\d+).*to.*"([^"]+)"'
            ],
            'complete': [
                r'complete.*task.*(\d+)',
                r'finish.*task.*(\d+)',
                r'done.*task.*(\d+)',
                r'mark.*task.*(\d+).*complete',
                r'mark.*task.*(\d+).*done'
            ],
            'list': [
                r'list.*tasks',
                r'show.*tasks',
                r'view.*tasks',
                r'all.*tasks',
                r'what.*tasks',
                r'display.*tasks'
            ]
        }
    
    def interpret_command(self, user_input: str) -> Dict:
        """
        Interpret a natural language command and return an action to take
        """
        user_input_lower = user_input.lower().strip()
        
        # Check each command type
        for cmd_type, patterns in self.commands.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower)
                if match:
                    if cmd_type == 'add':
                        task_title = match.group(1)
                        return {
                            'action': 'add_task',
                            'title': task_title,
                            'description': '',
                            'due_date': None
                        }
                    elif cmd_type == 'delete':
                        task_id = int(match.group(1))
                        return {
                            'action': 'delete_task',
                            'task_id': task_id
                        }
                    elif cmd_type == 'update':
                        task_id = int(match.group(1))
                        new_title = match.group(2)
                        return {
                            'action': 'update_task',
                            'task_id': task_id,
                            'title': new_title
                        }
                    elif cmd_type == 'complete':
                        task_id = int(match.group(1))
                        return {
                            'action': 'mark_complete',
                            'task_id': task_id
                        }
                    elif cmd_type == 'list':
                        return {
                            'action': 'view_tasks'
                        }
        
        # If no specific command is found, try to interpret as a new task if it's short
        if len(user_input) < 100 and not any(word in user_input_lower for word in 
              ['list', 'show', 'view', 'delete', 'remove', 'complete', 'done', 'finish', 'update', 'change', 'modify']):
            return {
                'action': 'add_task',
                'title': user_input,
                'description': '',
                'due_date': None
            }
        
        return {
            'action': 'unknown',
            'message': f"Could not understand command: {user_input}"
        }
    
    def execute_command(self, command_result: Dict, storage_path: str = "todos.json") -> Dict:
        """
        Execute the interpreted command and return the result
        """
        action = command_result.get('action')
        
        try:
            if action == 'add_task':
                title = command_result.get('title', '')
                description = command_result.get('description', '')
                due_date = command_result.get('due_date')
                
                if not title:
                    return {'success': False, 'message': 'Task title is required'}
                
                result = add_task(title, description, due_date, storage_path)
                return {
                    'success': True, 
                    'message': f"Added task: {result['title']} (ID: {result['id']})",
                    'task': result
                }
            
            elif action == 'delete_task':
                task_id = command_result.get('task_id')
                if task_id is None:
                    return {'success': False, 'message': 'Task ID is required for deletion'}
                
                success = delete_task(task_id, storage_path)
                if success:
                    return {'success': True, 'message': f"Deleted task with ID: {task_id}"}
                else:
                    return {'success': False, 'message': f"No task found with ID: {task_id}"}
            
            elif action == 'update_task':
                task_id = command_result.get('task_id')
                title = command_result.get('title')
                
                if task_id is None:
                    return {'success': False, 'message': 'Task ID is required for update'}
                if not title:
                    return {'success': False, 'message': 'New title is required for update'}
                
                result = update_task(task_id, title=title, storage_path=storage_path)
                if result:
                    return {
                        'success': True, 
                        'message': f"Updated task {task_id} to: {result['title']}",
                        'task': result
                    }
                else:
                    return {'success': False, 'message': f"No task found with ID: {task_id}"}
            
            elif action == 'mark_complete':
                task_id = command_result.get('task_id')
                if task_id is None:
                    return {'success': False, 'message': 'Task ID is required to mark complete'}
                
                result = mark_complete(task_id, storage_path=storage_path)
                if result:
                    status = "completed" if result['completed'] else "marked incomplete"
                    return {
                        'success': True, 
                        'message': f"Task {task_id} {status}",
                        'task': result
                    }
                else:
                    return {'success': False, 'message': f"No task found with ID: {task_id}"}
            
            elif action == 'view_tasks':
                tasks = view_tasks(storage_path=storage_path)
                if not tasks:
                    return {'success': True, 'message': 'No tasks found', 'tasks': []}
                
                task_list = []
                for task in tasks:
                    status = "✓" if task['completed'] else "○"
                    task_list.append(f"{status} [{task['id']}] {task['title']}")
                
                return {
                    'success': True, 
                    'message': f"Found {len(tasks)} task(s):",
                    'tasks': task_list
                }
            
            elif action == 'unknown':
                return {
                    'success': False,
                    'message': command_result.get('message', 'Unknown command')
                }
            
            else:
                return {
                    'success': False,
                    'message': f"Unsupported action: {action}"
                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"Error executing command: {str(e)}"
            }

def process_natural_language_command(user_input: str, storage_path: str = "todos.json") -> Dict:
    """
    Process a natural language command end-to-end
    """
    interpreter = TodoAIInterpreter()
    command_result = interpreter.interpret_command(user_input)
    execution_result = interpreter.execute_command(command_result, storage_path)
    return execution_result

def chatbot_response(user_input: str, storage_path: str = "todos.json") -> str:
    """
    Generate a chatbot response to user input
    """
    result = process_natural_language_command(user_input, storage_path)
    
    if result['success']:
        return result['message']
    else:
        return f"Sorry, I couldn't do that: {result['message']}"

# Convenience functions for direct use
def add_task_natural(user_input: str, storage_path: str = "todos.json") -> str:
    """Add a task using natural language processing"""
    return chatbot_response(user_input, storage_path)

def query_tasks_natural(user_input: str, storage_path: str = "todos.json") -> str:
    """Query tasks using natural language processing"""
    return chatbot_response(user_input, storage_path)