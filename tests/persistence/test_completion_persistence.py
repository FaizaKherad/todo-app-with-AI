"""
Unit tests for persistent task completion functionality.
"""
import json
import os
import tempfile
import pytest
from src.todo_engine.models import create_task, toggle_task_completion
from src.todo_engine.storage import storage
from src.todo_engine.persistence import FilePersistence


def test_completion_toggle_persists_to_file():
    """Test that toggling task completion status results in it being saved to the persistence file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add a task
        task = create_task("Completion Test Task", "Task for testing completion persistence")
        storage._tasks[task.id] = task
        storage.save_to_file()
        
        # Verify initial state
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['completed'] == False
        
        # Toggle completion status
        toggled_task = toggle_task_completion(task)
        storage._tasks[toggled_task.id] = toggled_task
        storage.save_to_file()
        
        # Verify the change was saved to the file
        updated_saved_tasks = persistence.load_tasks()
        assert len(updated_saved_tasks) == 1
        assert updated_saved_tasks[0]['completed'] == True
        assert updated_saved_tasks[0]['title'] == "Completion Test Task"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_completion_status_survives_application_restart():
    """Test that task completion status persists across application restarts."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add a task and save it
        original_task = create_task("Persistent Completion Task", "Task for completion test")
        storage._tasks[original_task.id] = original_task
        storage.save_to_file()
        
        # Toggle completion status and save
        completed_task = toggle_task_completion(original_task)
        storage._tasks[completed_task.id] = completed_task
        storage.save_to_file()
        
        # Simulate application restart by loading from file
        reloaded_tasks = persistence.load_tasks()
        
        # Verify the completion status persisted
        assert len(reloaded_tasks) == 1
        assert reloaded_tasks[0]['completed'] == True
        assert reloaded_tasks[0]['title'] == "Persistent Completion Task"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_completion_toggle_back_and_forth_persists():
    """Test that toggling completion status multiple times persists correctly."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new persistence instance with our temp file
        persistence = FilePersistence(temp_filename)
        
        # Add a task and save it
        original_task = create_task("Toggle Test Task", "Task for testing multiple toggles")
        storage._tasks[original_task.id] = original_task
        storage.save_to_file()
        
        # Verify initial state (should be False)
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['completed'] == False
        
        # Toggle to True
        task_completed = toggle_task_completion(original_task)
        storage._tasks[task_completed.id] = task_completed
        storage.save_to_file()
        
        # Verify state is True
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['completed'] == True
        
        # Toggle back to False
        task_uncompleted = toggle_task_completion(task_completed)
        storage._tasks[task_uncompleted.id] = task_uncompleted
        storage.save_to_file()
        
        # Verify state is False again
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['completed'] == False
        assert saved_tasks[0]['title'] == "Toggle Test Task"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)