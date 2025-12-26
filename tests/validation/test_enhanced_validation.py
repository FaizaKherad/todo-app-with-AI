"""
Unit tests for enhanced validation functionality.
"""
import pytest
from src.todo_engine.models import create_task, update_task, Task


def test_title_validation_min_length():
    """Test that titles must be at least 1 character."""
    # Test empty title (should fail)
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("", "Valid description")
    
    # Test single character title (should pass)
    task = create_task("A", "Valid description")
    assert task.title == "A"


def test_title_validation_max_length():
    """Test that titles cannot exceed 255 characters."""
    # Test 255 character title (should pass)
    long_title = "A" * 255
    task = create_task(long_title, "Valid description")
    assert task.title == long_title
    
    # Test 256 character title (should fail)
    too_long_title = "A" * 256
    with pytest.raises(ValueError, match="Title cannot exceed 255 characters"):
        create_task(too_long_title, "Valid description")


def test_description_validation_max_length():
    """Test that descriptions cannot exceed 1000 characters."""
    # Test 1000 character description (should pass)
    long_description = "D" * 1000
    task = create_task("Valid title", long_description)
    assert task.description == long_description
    
    # Test 1001 character description (should fail)
    too_long_description = "D" * 1001
    with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
        create_task("Valid title", too_long_description)


def test_update_task_title_validation():
    """Test that updating a task with invalid title fails."""
    # Create a valid task first
    original_task = create_task("Original Title", "Original Description")
    
    # Try to update with empty title (should fail)
    with pytest.raises(ValueError, match="Title cannot be empty"):
        update_task(original_task, "", "New description")
    
    # Try to update with too long title (should fail)
    with pytest.raises(ValueError, match="Title cannot exceed 255 characters"):
        update_task(original_task, "A" * 256, "New description")
    
    # Try to update with valid long title (should pass)
    valid_long_title = "A" * 255
    updated_task = update_task(original_task, valid_long_title, "New description")
    assert updated_task.title == valid_long_title


def test_update_task_description_validation():
    """Test that updating a task with invalid description fails."""
    # Create a valid task first
    original_task = create_task("Original Title", "Original Description")
    
    # Try to update with too long description (should fail)
    with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
        update_task(original_task, "New title", "D" * 1001)
    
    # Try to update with valid long description (should pass)
    valid_long_description = "D" * 1000
    updated_task = update_task(original_task, "New title", valid_long_description)
    assert updated_task.description == valid_long_description


def test_optional_description():
    """Test that description is optional and can be empty."""
    # Create task with empty description (should pass)
    task = create_task("Valid title", "")
    assert task.title == "Valid title"
    assert task.description == ""
    
    # Create task without description parameter (should pass)
    task = create_task("Valid title")
    assert task.title == "Valid title"
    assert task.description == ""


def test_task_model_validation():
    """Test that the Task model properly validates the enhanced constraints."""
    # Test creating a Task directly with valid constraints
    # Use a valid UUID for the id
    from uuid import uuid4
    valid_id = str(uuid4())
    task = Task(
        id=valid_id,
        title="Valid title",
        description="Valid description",
        completed=False,
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )
    assert task.title == "Valid title"

    # Test that the validation is applied during creation via create_task function
    long_title = "A" * 255
    long_description = "D" * 1000
    task = create_task(long_title, long_description)
    assert task.title == long_title
    assert task.description == long_description