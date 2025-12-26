"""
Unit tests for the MCP tools module
"""
import pytest
from src.todo_engine.mcp_tools import MCPTaskTools
import tempfile
import os


@pytest.fixture
def mcp_tools():
    """Create a fresh MCPTaskTools instance for each test."""
    # Temporarily change the persistence file to avoid conflicts with other tests
    from src.todo_engine import persistence, storage
    original_file = persistence.persistence.file_path

    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name

    # Update the persistence instance to use our temp file
    persistence.persistence = persistence.FilePersistence(temp_filename)

    # Create a fresh storage instance for the test
    from src.todo_engine.storage import FileStorage
    storage.storage = FileStorage()

    tools = MCPTaskTools()

    yield tools

    # Cleanup: restore original file and remove temp file
    persistence.persistence = persistence.FilePersistence(original_file)
    if os.path.exists(temp_filename):
        os.remove(temp_filename)


def test_add_task_success(mcp_tools):
    """Test that add_task successfully creates a task."""
    result = mcp_tools.add_task("Test task", "Test description")
    
    assert "id" in result
    assert result["title"] == "Test task"
    assert result["description"] == "Test description"
    assert result["completed"] == False
    assert "created_at" in result
    assert "updated_at" in result


def test_add_task_without_description(mcp_tools):
    """Test that add_task works when no description is provided."""
    result = mcp_tools.add_task("Test task")
    
    assert "id" in result
    assert result["title"] == "Test task"
    assert result["description"] == ""
    assert result["completed"] == False


def test_add_task_title_validation(mcp_tools):
    """Test that add_task validates title length."""
    # Test with a title that's too long
    long_title = "A" * 256
    with pytest.raises(ValueError, match="Title cannot exceed 255 characters"):
        mcp_tools.add_task(long_title, "Test description")
    
    # Test with an empty title
    with pytest.raises(ValueError, match="Title cannot be empty"):
        mcp_tools.add_task("", "Test description")


def test_add_task_description_validation(mcp_tools):
    """Test that add_task validates description length."""
    # Test with a description that's too long
    long_description = "D" * 1001
    with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
        mcp_tools.add_task("Test task", long_description)


def test_view_tasks_initially_empty(mcp_tools):
    """Test that view_tasks returns an empty list initially."""
    tasks = mcp_tools.view_tasks()
    
    assert tasks == []


def test_view_tasks_after_adding_task(mcp_tools):
    """Test that view_tasks returns added tasks."""
    # Add a task
    mcp_tools.add_task("Test task", "Test description")
    
    # View tasks
    tasks = mcp_tools.view_tasks()
    
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test task"
    assert tasks[0]["description"] == "Test description"


def test_update_task_success(mcp_tools):
    """Test that update_task successfully updates a task."""
    # Add a task first
    original_task = mcp_tools.add_task("Original task", "Original description")
    
    # Update the task
    updated_task = mcp_tools.update_task(
        original_task["id"], 
        "Updated task", 
        "Updated description"
    )
    
    assert updated_task["id"] == original_task["id"]
    assert updated_task["title"] == "Updated task"
    assert updated_task["description"] == "Updated description"


def test_update_task_partial_updates(mcp_tools):
    """Test that update_task can update just title or just description."""
    # Add a task first
    original_task = mcp_tools.add_task("Original task", "Original description")
    
    # Update just the title
    updated_task = mcp_tools.update_task(original_task["id"], "New title")
    
    assert updated_task["id"] == original_task["id"]
    assert updated_task["title"] == "New title"
    assert updated_task["description"] == "Original description"  # Should remain unchanged


def test_delete_task_success(mcp_tools):
    """Test that delete_task successfully deletes a task."""
    # Add a task first
    task = mcp_tools.add_task("Task to delete", "Description")
    
    # Verify it exists
    tasks = mcp_tools.view_tasks()
    assert len(tasks) == 1
    
    # Delete the task
    result = mcp_tools.delete_task(task["id"])
    
    assert result["deleted_task_id"] == task["id"]
    
    # Verify it's gone
    tasks = mcp_tools.view_tasks()
    assert len(tasks) == 0


def test_complete_task_success(mcp_tools):
    """Test that complete_task successfully toggles completion status."""
    # Add a task first
    task = mcp_tools.add_task("Task to complete", "Description")
    
    # Verify it's initially incomplete
    assert task["completed"] == False
    
    # Complete the task
    completed_task = mcp_tools.complete_task(task["id"])
    
    assert completed_task["id"] == task["id"]
    assert completed_task["completed"] == True


def test_task_completion_toggle(mcp_tools):
    """Test that complete_task toggles the completion status."""
    # Add a task first
    task = mcp_tools.add_task("Task to toggle", "Description")
    
    # Verify it's initially incomplete
    assert task["completed"] == False
    
    # Complete the task
    completed_task = mcp_tools.complete_task(task["id"])
    assert completed_task["completed"] == True
    
    # Complete it again (should toggle back to incomplete)
    incomplete_task = mcp_tools.complete_task(task["id"])
    assert incomplete_task["completed"] == False