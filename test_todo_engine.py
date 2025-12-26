"""
Test script to verify the Core Todo Engine functionality
"""
import json
from src.todo_engine.models import create_task, update_task, toggle_task_completion
from src.todo_engine.storage import storage


def test_task_creation():
    """Test creating a new task."""
    print("Testing task creation...")
    task = create_task("Test task", "This is a test task")
    print(f"Created task: {json.dumps(task.__dict__, indent=2)}")
    
    # Verify the task has the correct properties
    assert task.title == "Test task"
    assert task.description == "This is a test task"
    assert task.completed == False
    assert task.id is not None
    assert task.created_at == task.updated_at  # Should be the same when created
    
    print("PASS: Task creation test passed\n")


def test_storage():
    """Test storage functionality."""
    print("Testing storage...")
    
    # Add the task to storage
    task = create_task("Storage test", "Testing storage functionality")
    stored_task = storage.add_task(task)
    
    # Retrieve the task
    retrieved_task = storage.get_task(task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == task.title
    
    print(f"Stored and retrieved task: {json.dumps(retrieved_task.__dict__, indent=2)}")
    print("PASS: Storage test passed\n")


def test_update_task():
    """Test updating a task."""
    print("Testing task update...")
    
    # Create and store a task
    task = create_task("Original title", "Original description")
    storage.add_task(task)
    
    # Update the task
    updated_task = update_task(task, "Updated title", "Updated description")
    storage.update_task(task.id, updated_task)
    
    # Retrieve and verify the update
    retrieved_task = storage.get_task(task.id)
    assert retrieved_task.title == "Updated title"
    assert retrieved_task.description == "Updated description"
    assert retrieved_task.updated_at != retrieved_task.created_at
    
    print(f"Updated task: {json.dumps(retrieved_task.__dict__, indent=2)}")
    print("PASS: Task update test passed\n")


def test_toggle_completion():
    """Test toggling task completion."""
    print("Testing completion toggle...")
    
    # Create and store a task
    task = create_task("Toggle test", "Testing completion toggle")
    storage.add_task(task)
    
    # Toggle completion
    toggled_task = toggle_task_completion(task)
    storage.update_task(task.id, toggled_task)
    
    # Retrieve and verify the toggle
    retrieved_task = storage.get_task(task.id)
    assert retrieved_task.completed == True
    
    # Toggle again to make sure it works both ways
    toggled_task2 = toggle_task_completion(retrieved_task)
    storage.update_task(task.id, toggled_task2)
    
    retrieved_task2 = storage.get_task(task.id)
    assert retrieved_task2.completed == False
    
    print(f"First toggle (completed=True): {json.dumps(toggled_task.__dict__, indent=2)}")
    print(f"Second toggle (completed=False): {json.dumps(toggled_task2.__dict__, indent=2)}")
    print("PASS: Completion toggle test passed\n")


def test_delete_task():
    """Test deleting a task."""
    print("Testing task deletion...")
    
    # Create and store a task
    task = create_task("Deletion test", "Testing deletion functionality")
    storage.add_task(task)
    
    # Verify it exists
    retrieved_task = storage.get_task(task.id)
    assert retrieved_task is not None
    
    # Delete the task
    success = storage.delete_task(task.id)
    assert success == True
    
    # Verify it's gone
    retrieved_task = storage.get_task(task.id)
    assert retrieved_task is None
    
    print("PASS: Task deletion test passed\n")


def test_get_all_tasks():
    """Test retrieving all tasks."""
    print("Testing get all tasks...")
    
    # Clear any existing tasks
    storage.clear_all()
    
    # Add a few tasks
    task1 = create_task("Task 1", "First test task")
    task2 = create_task("Task 2", "Second test task")
    task3 = create_task("Task 3", "Third test task")
    
    storage.add_task(task1)
    storage.add_task(task2)
    storage.add_task(task3)
    
    # Get all tasks
    all_tasks = storage.get_all_tasks()
    assert len(all_tasks) == 3
    
    # Verify we have the right tasks
    titles = [task.title for task in all_tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles
    assert "Task 3" in titles
    
    print(f"All tasks ({len(all_tasks)}):")
    for task in all_tasks:
        print(f"  - {task.title}")
    print("PASS: Get all tasks test passed\n")


def run_all_tests():
    """Run all tests."""
    print("Running Core Todo Engine tests...\n")
    
    test_task_creation()
    test_storage()
    test_update_task()
    test_toggle_completion()
    test_delete_task()
    test_get_all_tasks()
    
    print("All tests passed! SUCCESS")


if __name__ == "__main__":
    run_all_tests()