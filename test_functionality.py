"""
Basic functionality tests for the Core Todo Engine CLI
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


def test_add_command():
    """Test the add command."""
    print("Testing ADD command...")
    
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "Test Task", 
        "--description", "Test description"
    ])
    
    assert exit_code == 0, f"Add command failed: {stderr}"
    
    # Parse the output
    try:
        task_data = json.loads(stdout)
        assert task_data["title"] == "Test Task"
        assert task_data["description"] == "Test description"
        assert task_data["completed"] == False
        assert "id" in task_data
        assert len(task_data["id"]) > 0
        print(f"  PASS: Successfully added task: {task_data['title']}")
    except json.JSONDecodeError:
        assert False, f"Add output is not valid JSON: {stdout}"
    
    print("  PASS: Add command test\n")


def test_list_command():
    """Test the list command."""
    print("Testing LIST command...")
    
    stdout, stderr, exit_code = run_cli_command(["list"])
    
    assert exit_code == 0, f"List command failed: {stderr}"
    
    # Parse the output (should be an empty array in a new process)
    try:
        tasks = json.loads(stdout)
        assert isinstance(tasks, list), "Output should be an array"
        print(f"  PASS: Successfully retrieved {len(tasks)} tasks")
    except json.JSONDecodeError:
        assert False, f"List output is not valid JSON: {stdout}"
    
    print("  PASS: List command test\n")


def test_update_command_with_invalid_id():
    """Test the update command with an invalid ID."""
    print("Testing UPDATE command with invalid ID...")
    
    stdout, stderr, exit_code = run_cli_command([
        "update",
        "--id", "invalid-id",
        "--title", "Updated Title"
    ])
    
    # This should fail with exit code 1 (not 0) since the task doesn't exist
    # Our CLI should return exit code 10 for TASK_NOT_FOUND
    # But in a new process, the task won't exist
    assert exit_code != 0, "Expected update to fail for non-existent task"
    
    print(f"  PASS: Update correctly failed for non-existent task (exit code: {exit_code})")
    print("  PASS: Update with invalid ID test\n")


def test_delete_command_with_invalid_id():
    """Test the delete command with an invalid ID."""
    print("Testing DELETE command with invalid ID...")
    
    stdout, stderr, exit_code = run_cli_command([
        "delete",
        "--id", "invalid-id"
    ])
    
    # This should fail since the task doesn't exist
    assert exit_code != 0, "Expected delete to fail for non-existent task"
    
    print(f"  PASS: Delete correctly failed for non-existent task (exit code: {exit_code})")
    print("  PASS: Delete with invalid ID test\n")


def test_complete_command_with_invalid_id():
    """Test the complete command with an invalid ID."""
    print("Testing COMPLETE command with invalid ID...")
    
    stdout, stderr, exit_code = run_cli_command([
        "complete",
        "--id", "invalid-id"
    ])
    
    # This should fail since the task doesn't exist
    assert exit_code != 0, "Expected complete to fail for non-existent task"
    
    print(f"  PASS: Complete correctly failed for non-existent task (exit code: {exit_code})")
    print("  PASS: Complete with invalid ID test\n")


def test_title_validation():
    """Test title validation."""
    print("Testing title validation...")
    
    # Test empty title
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", "", 
        "--description", "This should fail"
    ])
    
    # argparse validation should catch this
    assert exit_code != 0, "Expected validation error for empty title"
    assert "Title cannot be empty" in stderr or "error" in stderr.lower()
    print("  ✓ Empty title correctly rejected")
    
    # Test title too long
    long_title = "a" * 101  # 101 characters, exceeding the 100 limit
    stdout, stderr, exit_code = run_cli_command([
        "add", 
        "--title", long_title, 
        "--description", "This should fail"
    ])
    
    # argparse validation should catch this
    assert exit_code != 0, "Expected validation error for long title"
    assert "Title cannot exceed" in stderr or "error" in stderr.lower()
    print("  ✓ Long title correctly rejected")
    
    print("  PASS: Title validation test\n")


def run_all_functionality_tests():
    """Run all functionality tests."""
    print("Running functionality tests for Core Todo Engine CLI...\n")
    
    test_add_command()
    test_list_command()
    test_update_command_with_invalid_id()
    test_delete_command_with_invalid_id()
    test_complete_command_with_invalid_id()
    test_title_validation()
    
    print("All functionality tests passed! SUCCESS")


if __name__ == "__main__":
    run_all_functionality_tests()