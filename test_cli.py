"""
Comprehensive CLI tests for the Core Todo Engine
"""
import subprocess
import json
import sys
import os
from io import StringIO
from unittest.mock import patch


def run_cli_command(args):
    """
    Run a CLI command and return the output and exit code.
    
    Args:
        args: List of command arguments
        
    Returns:
        tuple: (stdout, stderr, exit_code)
    """
    # Prepare the command
    cmd = [sys.executable, "main.py"] + args
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return result.stdout, result.stderr, result.returncode


def test_cli_add_task():
    """Test adding a task via CLI."""
    print("Testing CLI add task...")
    
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "CLI Test Task", 
        "--description", "Testing CLI functionality"
    ])
    
    # Check that it succeeded
    assert exit_code == 0, f"Add command failed with exit code {exit_code}, stderr: {stderr}"
    
    # Parse the output as JSON
    try:
        task_data = json.loads(stdout)
        assert task_data["title"] == "CLI Test Task"
        assert task_data["description"] == "Testing CLI functionality"
        assert task_data["completed"] == False
        assert "id" in task_data
        print(f"  Added task: {task_data['title']}")
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON: {stdout}"
    
    print("  PASS: CLI add task test\n")


def test_cli_list_tasks():
    """Test listing tasks via CLI."""
    print("Testing CLI list tasks...")
    
    stdout, stderr, exit_code = run_cli_command(["list"])
    
    # Check that it succeeded
    assert exit_code == 0, f"List command failed with exit code {exit_code}, stderr: {stderr}"
    
    # Parse the output as JSON (should be an array)
    try:
        tasks_data = json.loads(stdout)
        assert isinstance(tasks_data, list), "Output should be an array of tasks"
        print(f"  Found {len(tasks_data)} tasks")
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON: {stdout}"
    
    print("  PASS: CLI list tasks test\n")


def test_cli_invalid_title():
    """Test CLI with invalid title (empty)."""
    print("Testing CLI with invalid title...")
    
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "", 
        "--description", "This should fail"
    ])
    
    # Should fail with exit code 11 (invalid title)
    assert exit_code == 11, f"Expected exit code 11, got {exit_code}"
    assert "INVALID_TITLE" in stderr, f"Expected INVALID_TITLE error, got: {stderr}"
    
    print("  PASS: CLI invalid title test\n")


def test_cli_task_not_found():
    """Test CLI operations on non-existent task."""
    print("Testing CLI with non-existent task ID...")
    
    # Try to update a non-existent task
    stdout, stderr, exit_code = run_cli_command([
        "update", 
        "--id", "non-existent-id", 
        "--title", "Updated title"
    ])
    
    # Should fail with exit code 10 (task not found)
    assert exit_code == 10, f"Expected exit code 10, got {exit_code}"
    assert "TASK_NOT_FOUND" in stderr, f"Expected TASK_NOT_FOUND error, got: {stderr}"
    
    print("  PASS: CLI task not found test\n")


def test_cli_complete_task():
    """Test completing a task via CLI."""
    print("Testing CLI complete task...")
    
    # First, add a task
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "Task to complete", 
        "--description", "Testing completion"
    ])
    
    assert exit_code == 0, f"Add command failed: {stderr}"
    
    # Parse the task to get its ID
    try:
        task_data = json.loads(stdout)
        task_id = task_data["id"]
    except json.JSONDecodeError:
        assert False, f"Add output is not valid JSON: {stdout}"
    
    # Now complete the task
    stdout, stderr, exit_code = run_cli_command([
        "complete", 
        "--id", task_id
    ])
    
    # Should succeed
    assert exit_code == 0, f"Complete command failed: {stderr}"
    
    # Check that the task is now completed
    try:
        completed_task = json.loads(stdout)
        assert completed_task["id"] == task_id
        assert completed_task["completed"] == True
        print(f"  Completed task: {completed_task['title']}")
    except json.JSONDecodeError:
        assert False, f"Complete output is not valid JSON: {stdout}"
    
    print("  PASS: CLI complete task test\n")


def run_all_cli_tests():
    """Run all CLI tests."""
    print("Running CLI tests for Core Todo Engine...\n")
    
    test_cli_add_task()
    test_cli_list_tasks()
    test_cli_invalid_title()
    test_cli_task_not_found()
    test_cli_complete_task()
    
    print("All CLI tests passed! SUCCESS")


if __name__ == "__main__":
    run_all_cli_tests()