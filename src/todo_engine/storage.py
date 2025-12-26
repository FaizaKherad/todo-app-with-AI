"""
File-based storage implementation for the Todo Engine with cloud persistence
Supports concurrent access patterns for multi-pod environments
"""
import threading
from typing import Dict, List, Optional
from .models import Task
from .persistence import persistence


class FileStorage:
    """
    File-based storage for tasks with cloud-compatible persistence.
    Uses thread-safe operations to handle concurrent access in multi-pod environments.
    """
    def __init__(self):
        # Load tasks from file on initialization
        self._tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()  # Thread-safe lock for concurrent access

        try:
            self.load_from_file()
        except Exception as e:
            # If loading fails, start with empty storage
            # Log the error if logging is available
            self._tasks = {}

    def load_from_file(self):
        """Load tasks from the persistence file."""
        with self._lock:  # Ensure thread safety during file read
            try:
                tasks_data = persistence.load_tasks()
                self._tasks = {}
                for task_data in tasks_data:
                    # Create Task instance from loaded data
                    task = Task(
                        id=task_data['id'],
                        title=task_data['title'],
                        description=task_data.get('description', ''),
                        completed=task_data.get('completed', False),
                        created_at=task_data['created_at'],
                        updated_at=task_data['updated_at']
                    )
                    self._tasks[task.id] = task
            except Exception as e:
                # If loading fails, start with empty storage
                # TODO: Consider logging this error
                self._tasks = {}

    def save_to_file(self):
        """Save all tasks to the persistence file."""
        with self._lock:  # Ensure thread safety during file write
            try:
                tasks_data = []
                for task in self._tasks.values():
                    task_data = {
                        'id': task.id,
                        'title': task.title,
                        'description': task.description,
                        'completed': task.completed,
                        'created_at': task.created_at,
                        'updated_at': task.updated_at
                    }
                    tasks_data.append(task_data)

                persistence.save_tasks(tasks_data)
            except Exception as e:
                raise Exception(f"PERSISTENCE_WRITE_FAILED: {str(e)}")

    def add_task(self, task: Task) -> Task:
        """
        Add a task to the storage and persist to file.

        Args:
            task: The task to add

        Returns:
            Task: The added task
        """
        with self._lock:  # Ensure thread safety during add operation
            self._tasks[task.id] = task
            try:
                self.save_to_file()
            except Exception as e:
                # If save fails, remove the task from memory to maintain consistency
                if task.id in self._tasks:
                    del self._tasks[task.id]
                raise e
            return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The task if found, None otherwise
        """
        with self._lock:  # Ensure thread safety during read operation
            return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the storage.

        Returns:
            List[Task]: All tasks in the storage
        """
        with self._lock:  # Ensure thread safety during read operation
            return list(self._tasks.values())

    def update_task(self, task_id: str, updated_task: Task) -> Optional[Task]:
        """
        Update a task in the storage and persist to file.

        Args:
            task_id: The ID of the task to update
            updated_task: The updated task object

        Returns:
            Task: The updated task if successful, None if task not found
        """
        with self._lock:  # Ensure thread safety during update operation
            if task_id not in self._tasks:
                return None

            # Store the original task in case save fails
            original_task = self._tasks[task_id]

            self._tasks[task_id] = updated_task
            try:
                self.save_to_file()
            except Exception as e:
                # If save fails, restore the original task to maintain consistency
                self._tasks[task_id] = original_task
                raise e
            return updated_task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from the storage and persist to file.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if not found
        """
        with self._lock:  # Ensure thread safety during delete operation
            if task_id in self._tasks:
                # Store the task in case save fails
                deleted_task = self._tasks[task_id]
                del self._tasks[task_id]
                try:
                    self.save_to_file()
                except Exception as e:
                    # If save fails, restore the task to maintain consistency
                    self._tasks[task_id] = deleted_task
                    raise e
                return True
            return False

    def clear_all(self):
        """
        Clear all tasks from storage (for testing purposes).
        """
        with self._lock:  # Ensure thread safety during clear operation
            self._tasks.clear()
            self.save_to_file()


# Global instance of storage for the application
storage = FileStorage()


def reset_global_storage_for_testing():
    """
    Reset the global storage instance for testing purposes.
    This clears all tasks and reloads from the default persistence file.
    """
    global storage
    storage = FileStorage()