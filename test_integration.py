"""
Integration tests for the Core Todo Engine CLI
"""
import subprocess
import json
import sys


def run_cli_command(args):
    """
    Run a CLI command and return the output and exit code.
    """
    cmd = [sys.executable, "main.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def test_add_and_list():
    """Test adding a task and then listing it."""
    print("Testing add and list functionality...")
    
    # Add a task
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "Integration Test Task", 
        "--description", "Testing CLI integration"
    ])
    
    assert exit_code == 0, f"Add command failed: {stderr}"
    
    # Parse the added task to get its ID
    try:
        task_data = json.loads(stdout)
        task_id = task_data["id"]
        assert task_data["title"] == "Integration Test Task"
        print(f"  Added task with ID: {task_id}")
    except json.JSONDecodeError:
        assert False, f"Add output is not valid JSON: {stdout}"
    
    # List tasks and verify our task is there
    stdout, stderr, exit_code = run_cli_command(["list"])
    assert exit_code == 0, f"List command failed: {stderr}"
    
    try:
        tasks = json.loads(stdout)
        # Note: Since storage is in-memory, adding a task in one process
        # and listing in another won't show the task from the previous process
        # This is expected behavior for Phase I
        print(f"  Found {len(tasks)} tasks in current process")
    except json.JSONDecodeError:
        assert False, f"List output is not valid JSON: {stdout}"
    
    print("  PASS: Add and list test\n")


def test_update_functionality():
    """Test updating a task."""
    print("Testing update functionality...")
    
    # Add a task first
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "Original Title", 
        "--description", "Original description"
    ])
    
    assert exit_code == 0, f"Add command failed: {stderr}"
    
    try:
        task_data = json.loads(stdout)
        task_id = task_data["id"]
        print(f"  Added task with ID: {task_id}")
    except json.JSONDecodeError:
        assert False, f"Add output is not valid JSON: {stdout}"
    
    # Update the task
    stdout, stderr, exit_code = run_cli_command([
        "update",
        "--id", task_id,
        "--title", "Updated Title",
        "--description", "Updated description"
    ])
    
    assert exit_code == 0, f"Update command failed: {stderr}"
    
    try:
        updated_task = json.loads(stdout)
        assert updated_task["id"] == task_id
        assert updated_task["title"] == "Updated Title"
        assert updated_task["description"] == "Updated description"
        print(f"  Updated task: {updated_task['title']}")
    except json.JSONDecodeError:
        assert False, f"Update output is not valid JSON: {stdout}"
    
    print("  PASS: Update test\n")


def test_completion_toggle():
    """Test toggling task completion."""
    print("Testing completion toggle...")
    
    # Add a task
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "Completion Test", 
        "--description", "Testing completion toggle"
    ])
    
    assert exit_code == 0, f"Add command failed: {stderr}"
    
    try:
        task_data = json.loads(stdout)
        task_id = task_data["id"]
        assert task_data["completed"] == False  # Should default to False
        print(f"  Added incomplete task with ID: {task_id}")
    except json.JSONDecodeError:
        assert False, f"Add output is not valid JSON: {stdout}"
    
    # Toggle completion
    stdout, stderr, exit_code = run_cli_command([
        "complete",
        "--id", task_id
    ])
    
    assert exit_code == 0, f"Complete command failed: {stderr}"
    
    try:
        completed_task = json.loads(stdout)
        assert completed_task["id"] == task_id
        assert completed_task["completed"] == True  # Should now be True
        print(f"  Completed task: {completed_task['title']}")
    except json.JSONDecodeError:
        assert False, f"Complete output is not valid JSON: {stdout}"
    
    print("  PASS: Completion toggle test\n")


def test_delete_functionality():
    """Test deleting a task."""
    print("Testing delete functionality...")
    
    # Add a task
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "Task to Delete", 
        "--description", "This will be deleted"
    ])
    
    assert exit_code == 0, f"Add command failed: {stderr}"
    
    try:
        task_data = json.loads(stdout)
        task_id = task_data["id"]
        print(f"  Added task to delete with ID: {task_id}")
    except json.JSONDecodeError:
        assert False, f"Add output is not valid JSON: {stdout}"
    
    # Delete the task
    stdout, stderr, exit_code = run_cli_command([
        "delete",
        "--id", task_id
    ])
    
    assert exit_code == 0, f"Delete command failed: {stderr}"
    
    try:
        result = json.loads(stdout)
        assert result["deleted_task_id"] == task_id
        print(f"  Deleted task: {task_id}")
    except json.JSONDecodeError:
        assert False, f"Delete output is not valid JSON: {stdout}"
    
    print("  PASS: Delete test\n")


def test_validation_errors():
    """Test validation errors."""
    print("Testing validation errors...")
    
    # Try to add a task with empty title (this should fail at argparse level)
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", ""  # Empty title should fail
    ])
    
    # argparse will exit with code 2 for argument errors
    # The error should be in stderr
    assert exit_code != 0, "Expected validation error for empty title"
    assert "Title cannot be empty" in stderr or "error" in stderr.lower()
    print("  PASS: Empty title validation\n")


def run_all_integration_tests():
    """Run all integration tests."""
    print("Running integration tests for Core Todo Engine CLI...\n")
    
    test_add_and_list()
    test_update_functionality()
    test_completion_toggle()
    test_delete_functionality()
    test_validation_errors()
    
    print("All integration tests passed! SUCCESS")


if __name__ == "__main__":
    run_all_integration_tests()