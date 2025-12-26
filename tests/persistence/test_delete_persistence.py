"""
Unit tests for persistent task deletion functionality.
"""
import json
import os
import tempfile
import pytest
from src.todo_engine.models import create_task
from src.todo_engine.storage import storage
from src.todo_engine.persistence import FilePersistence


def test_delete_task_persists_to_file():
    """Test that deleting a task results in it being removed from the persistence file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add multiple tasks
        task1 = create_task("Task 1", "Description 1")
        task2 = create_task("Task 2", "Description 2")
        task3 = create_task("Task 3", "Description 3")
        
        storage._tasks[task1.id] = task1
        storage._tasks[task2.id] = task2
        storage._tasks[task3.id] = task3
        storage.save_to_file()
        
        # Verify all tasks are in the file
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 3
        
        # Delete one task
        del storage._tasks[task2.id]
        storage.save_to_file()
        
        # Verify the task was removed from the file
        updated_saved_tasks = persistence.load_tasks()
        assert len(updated_saved_tasks) == 2
        
        # Verify the correct task was deleted
        titles = [task['title'] for task in updated_saved_tasks]
        assert "Task 1" in titles
        assert "Task 2" not in titles  # This should be deleted
        assert "Task 3" in titles
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_deleted_task_stays_deleted_after_restart():
    """Test that a deleted task remains deleted after application restart."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add multiple tasks
        task1 = create_task("Task 1", "Description 1")
        task2 = create_task("Task 2", "Description 2")
        
        storage._tasks[task1.id] = task1
        storage._tasks[task2.id] = task2
        storage.save_to_file()
        
        # Delete one task and save
        del storage._tasks[task2.id]
        storage.save_to_file()
        
        # Simulate application restart by loading from file
        reloaded_tasks = persistence.load_tasks()
        
        # Verify the deletion persisted
        assert len(reloaded_tasks) == 1
        assert reloaded_tasks[0]['title'] == "Task 1"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_delete_nonexistent_task_not_saved():
    """Test that attempting to delete a non-existent task doesn't affect the file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add one task
        task1 = create_task("Task 1", "Description 1")
        storage._tasks[task1.id] = task1
        storage.save_to_file()
        
        # Verify the task is in the file
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        
        # Attempt to delete a non-existent task (should not affect storage)
        nonexistent_id = "nonexistent-id"
        if nonexistent_id in storage._tasks:
            del storage._tasks[nonexistent_id]
            storage.save_to_file()
        
        # Verify the file still contains the original task
        updated_saved_tasks = persistence.load_tasks()
        assert len(updated_saved_tasks) == 1
        assert updated_saved_tasks[0]['title'] == "Task 1"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)