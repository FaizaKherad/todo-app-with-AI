"""
Unit tests for persistent task creation functionality.
"""
import json
import os
import tempfile
import pytest
from src.todo_engine.models import create_task
from src.todo_engine.storage import FileStorage
from src.todo_engine.persistence import FilePersistence


def test_add_task_persists_to_file():
    """Test that adding a task results in it being saved to the persistence file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name

    # Create a custom persistence instance for testing
    test_persistence = FilePersistence(temp_filename)

    try:
        # Create a new storage instance that uses our temporary file
        # We'll need to create a temporary file named "tasks.json" in a temp directory
        temp_dir = os.path.dirname(temp_filename)
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        # Create storage that will use our temp file (named tasks.json)
        os.rename(temp_filename, "tasks.json")
        storage = FileStorage()

        # Add a task using the storage
        task = create_task("Test Task", "Test Description")
        storage.add_task(task)  # Use the proper API

        # Verify the task was saved to the file
        saved_tasks = test_persistence.load_tasks()
        assert len(saved_tasks) == 1
        assert saved_tasks[0]['title'] == "Test Task"
        assert saved_tasks[0]['description'] == "Test Description"

    finally:
        # Restore original directory
        os.chdir(original_cwd)
        # Clean up any files created in temp directory
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")
        if os.path.exists(temp_filename):  # In case rename failed
            os.remove(temp_filename)


def test_task_survives_application_restart():
    """Test that a task persists across application restarts (simulated by creating new storage)."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name

    # Create a custom persistence instance for testing
    test_persistence = FilePersistence(temp_filename)

    try:
        # Create a new storage instance that uses our temporary file
        temp_dir = os.path.dirname(temp_filename)
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        # Create storage that will use our temp file (named tasks.json)
        os.rename(temp_filename, "tasks.json")
        storage1 = FileStorage()

        # Add a task
        task = create_task("Persistent Task", "This should survive restart")
        storage1.add_task(task)

        # Simulate application restart by creating a new storage instance
        # which will load from the same file
        storage2 = FileStorage()
        all_tasks = storage2.get_all_tasks()

        # Verify the task exists in the loaded data
        assert len(all_tasks) == 1
        assert all_tasks[0].title == "Persistent Task"
        assert all_tasks[0].description == "This should survive restart"

    finally:
        # Restore original directory
        os.chdir(original_cwd)
        # Clean up any files created in temp directory
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")
        if os.path.exists(temp_filename):  # In case rename failed
            os.remove(temp_filename)


def test_multiple_tasks_persist():
    """Test that multiple tasks are all saved to the file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name

    # Create a custom persistence instance for testing
    test_persistence = FilePersistence(temp_filename)

    try:
        # Create a new storage instance that uses our temporary file
        temp_dir = os.path.dirname(temp_filename)
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        # Create storage that will use our temp file (named tasks.json)
        os.rename(temp_filename, "tasks.json")
        storage = FileStorage()

        # Add multiple tasks using the proper API
        task1 = create_task("Task 1", "First task")
        task2 = create_task("Task 2", "Second task")
        task3 = create_task("Task 3", "Third task")

        storage.add_task(task1)
        storage.add_task(task2)
        storage.add_task(task3)

        # Verify all tasks were saved by creating a new storage instance
        # and checking what was persisted
        new_storage = FileStorage()
        all_tasks = new_storage.get_all_tasks()
        assert len(all_tasks) == 3
        titles = [task.title for task in all_tasks]
        assert "Task 1" in titles
        assert "Task 2" in titles
        assert "Task 3" in titles

    finally:
        # Restore original directory
        os.chdir(original_cwd)
        # Clean up any files created in temp directory
        if os.path.exists("tasks.json"):
            os.remove("tasks.json")
        if os.path.exists(temp_filename):  # In case rename failed
            os.remove(temp_filename)