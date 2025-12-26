"""
Unit tests for persistent task update functionality.
"""
import json
import os
import tempfile
import pytest
from src.todo_engine.models import create_task, update_task
from src.todo_engine.storage import storage
from src.todo_engine.persistence import FilePersistence


def test_update_task_persists_to_file():
    """Test that updating a task results in it being saved to the persistence file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add a task first
        original_task = create_task("Original Task", "Original Description")
        storage._tasks[original_task.id] = original_task
        storage.save_to_file()
        
        # Verify it's in the file
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['title'] == "Original Task"
        
        # Update the task
        updated_task = update_task(original_task, "Updated Task", "Updated Description")
        storage._tasks[updated_task.id] = updated_task
        storage.save_to_file()
        
        # Verify the update was saved to the file
        updated_saved_tasks = persistence.load_tasks()
        assert len(updated_saved_tasks) == 1
        assert updated_saved_tasks[0]['title'] == "Updated Task"
        assert updated_saved_tasks[0]['description'] == "Updated Description"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_updated_task_survives_application_restart():
    """Test that an updated task persists across application restarts."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add a task and save it
        original_task = create_task("Original Task", "Original Description")
        storage._tasks[original_task.id] = original_task
        storage.save_to_file()
        
        # Update the task and save again
        updated_task = update_task(original_task, "Updated Task", "Updated Description")
        storage._tasks[updated_task.id] = updated_task
        storage.save_to_file()
        
        # Simulate application restart by loading from file
        reloaded_tasks = persistence.load_tasks()
        
        # Verify the update persisted
        assert len(reloaded_tasks) == 1
        assert reloaded_tasks[0]['title'] == "Updated Task"
        assert reloaded_tasks[0]['description'] == "Updated Description"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_partial_update_persists():
    """Test that updating only the title or description works correctly."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add a task and save it
        original_task = create_task("Original Task", "Original Description")
        storage._tasks[original_task.id] = original_task
        storage.save_to_file()
        
        # Update only the title
        updated_task = update_task(original_task, "Updated Title", None)
        storage._tasks[updated_task.id] = updated_task
        storage.save_to_file()
        
        # Verify the update was saved
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['title'] == "Updated Title"
        assert saved_tasks[0]['description'] == "Original Description"  # Should remain unchanged
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)