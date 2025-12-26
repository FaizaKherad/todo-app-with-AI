"""
Todo Management Skill for Qwen
Provides core functionality for managing todos as specified in the project constitution
"""

import json
import os
from datetime import datetime

class TodoManager:
    def __init__(self, storage_path="todos.json"):
        self.storage_path = storage_path
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Load todos from storage"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_todos(self):
        """Save todos to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def add_task(self, title, description="", due_date=None):
        """Add a new task to the list - Core functionality from constitution"""
        task = {
            "id": len(self.todos) + 1,
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(task)
        self.save_todos()
        return task
    
    def delete_task(self, task_id):
        """Delete a task from the list - Core functionality from constitution"""
        original_count = len(self.todos)
        self.todos = [task for task in self.todos if task["id"] != task_id]
        
        if len(self.todos) < original_count:
            self.save_todos()
            return True  # Task was deleted
        return False  # Task not found
    
    def update_task(self, task_id, title=None, description=None, due_date=None):
        """Update task details - Core functionality from constitution"""
        for task in self.todos:
            if task["id"] == task_id:
                if title is not None:
                    task["title"] = title
                if description is not None:
                    task["description"] = description
                if due_date is not None:
                    task["due_date"] = due_date
                self.save_todos()
                return task
        return None  # Task not found
    
    def view_tasks(self, completed=None):
        """Display all tasks or filter by completion status - Core functionality from constitution"""
        if completed is None:
            return self.todos
        return [task for task in self.todos if task["completed"] == completed]
    
    def mark_complete(self, task_id, completed=True):
        """Toggle task completion state - Core functionality from constitution"""
        for task in self.todos:
            if task["id"] == task_id:
                task["completed"] = completed
                self.save_todos()
                return task
        return None  # Task not found

def create_todo_manager(storage_path="todos.json"):
    """Factory function to create a TodoManager instance"""
    return TodoManager(storage_path)

def add_task(title, description="", due_date=None, storage_path="todos.json"):
    """Add a new task - convenience function"""
    tm = TodoManager(storage_path)
    return tm.add_task(title, description, due_date)

def delete_task(task_id, storage_path="todos.json"):
    """Delete a task - convenience function"""
    tm = TodoManager(storage_path)
    return tm.delete_task(task_id)

def update_task(task_id, title=None, description=None, due_date=None, storage_path="todos.json"):
    """Update a task - convenience function"""
    tm = TodoManager(storage_path)
    return tm.update_task(task_id, title, description, due_date)

def view_tasks(completed=None, storage_path="todos.json"):
    """View tasks - convenience function"""
    tm = TodoManager(storage_path)
    return tm.view_tasks(completed)

def mark_complete(task_id, completed=True, storage_path="todos.json"):
    """Mark task as complete/incomplete - convenience function"""
    tm = TodoManager(storage_path)
    return tm.mark_complete(task_id, completed)