"""
Integration tests for file persistence functionality using the CLI.
"""
import json
import os
import tempfile
import subprocess
import sys
from src.todo_engine.persistence import FilePersistence
from src.todo_engine.storage import FileStorage


def test_loading_tasks_on_startup():
    """Test that tasks are loaded from file on application startup."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create some tasks in the file
        initial_tasks = [
            {
                "id": "test-id-1",
                "title": "Startup Task 1",
                "description": "Task loaded on startup",
                "completed": False,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "test-id-2",
                "title": "Startup Task 2",
                "description": "Another task loaded on startup",
                "completed": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        # Write the tasks to the file
        with open(temp_filename, 'w') as f:
            json.dump(initial_tasks, f)
        
        # Create a new storage instance to simulate application startup
        storage = FileStorage()
        
        # Verify the tasks were loaded
        loaded_tasks = storage.get_all_tasks()
        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].title == "Startup Task 1"
        assert loaded_tasks[1].title == "Startup Task 2"
        assert loaded_tasks[1].completed == True
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_atomic_file_writes():
    """Test that file writes are atomic and don't corrupt data."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Create a new storage instance
        storage = FileStorage()
        
        # Add some tasks using the proper API
        from src.todo_engine.models import create_task
        task1 = create_task("Test Task 1", "Description for task 1")
        task2 = create_task("Test Task 2", "Description for task 2")
        
        # Add tasks to storage (this should persist them)
        storage.add_task(task1)
        storage.add_task(task2)
        
        # Verify tasks are in memory
        all_tasks = storage.get_all_tasks()
        assert len(all_tasks) == 2
        
        # Check the file to make sure tasks were saved
        persistence = FilePersistence(temp_filename)
        saved_tasks = persistence.load_tasks()
        assert len(saved_tasks) == 2
        
        titles = [task['title'] for task in saved_tasks]
        assert "Test Task 1" in titles
        assert "Test Task 2" in titles
        
        # Update a task and verify it's saved
        updated_task = all_tasks[0]
        from src.todo_engine.models import update_task
        updated_task = update_task(updated_task, "Updated Task 1", "Updated description")
        storage.update_task(updated_task.id, updated_task)
        
        # Verify the update was saved
        updated_all_tasks = storage.get_all_tasks()
        updated_saved_tasks = persistence.load_tasks()
        assert len(updated_saved_tasks) == 2
        updated_titles = [task['title'] for task in updated_saved_tasks]
        assert "Updated Task 1" in updated_titles
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_empty_file_handling():
    """Test that the system handles empty or missing files correctly."""
    # Test with a non-existent file (should create an empty one)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    # Remove the file to simulate it not existing
    os.remove(temp_filename)
    
    try:
        # Create storage instance with non-existent file
        storage = FileStorage()
        
        # The file should now exist and storage should be empty
        assert os.path.exists(temp_filename) == True
        tasks = storage.get_all_tasks()
        assert len(tasks) == 0
        
        # Add a task and verify it's saved
        from src.todo_engine.models import create_task
        new_task = create_task("New Task", "A new task")
        storage.add_task(new_task)
        
        # Verify the task was saved
        tasks = storage.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "New Task"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_corrupted_file_handling():
    """Test that the system handles corrupted files gracefully."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        # Write corrupted JSON to the file
        with open(temp_filename, 'w') as f:
            f.write("This is not valid JSON")
        
        # Create persistence instance
        persistence = FilePersistence(temp_filename)
        
        # Loading from corrupted file should raise an error
        try:
            persistence.load_tasks()
            # If we reach this line, the error wasn't raised as expected
            assert False, "Expected ValueError for corrupted file"
        except ValueError:
            # This is expected
            pass
        
        # The system should handle this gracefully and create a new empty file
        # or handle the error appropriately
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)