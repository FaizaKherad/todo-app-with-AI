"""
Performance tests for the Todo application in cloud environment
Verifies that file operations complete within 2 seconds even with 1000 tasks
"""
import time
import json
import tempfile
import os
from src.todo_engine.models import create_task
from src.todo_engine.storage import FileStorage


def test_performance_with_1000_tasks():
    """
    Test that file operations complete within 2 seconds for 1000 tasks.
    """
    # Use a temporary file for testing to avoid affecting the main tasks.json
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name

    # Create a new storage instance that uses our temporary file
    from src.todo_engine import persistence
    original_file_path = persistence.persistence.file_path
    try:
        # Temporarily replace the persistence instance with our temp file
        original_persistence = persistence.persistence
        persistence.persistence = persistence.FilePersistence(temp_filename)

        # Create a new storage instance with the temporary persistence
        test_storage = FileStorage()

        print("Testing performance with 1000 tasks...")
        
        # Measure time to add 1000 tasks
        start_time = time.time()
        
        for i in range(1000):
            task = create_task(f"Task {i}", f"Description for task {i}")
            test_storage.add_task(task)
        
        end_time = time.time()
        add_time = end_time - start_time
        
        print(f"Time to add 1000 tasks: {add_time:.2f} seconds")
        
        # Verify all tasks were added
        all_tasks = test_storage.get_all_tasks()
        assert len(all_tasks) == 1000, f"Expected 1000 tasks, got {len(all_tasks)}"
        
        # Measure time to get all tasks
        start_time = time.time()
        tasks = test_storage.get_all_tasks()
        end_time = time.time()
        get_time = end_time - start_time
        
        print(f"Time to retrieve 1000 tasks: {get_time:.2f} seconds")
        
        # Measure time to update all tasks
        start_time = time.time()
        
        for i, task in enumerate(tasks):
            # Update each task with a new title
            updated_task = test_storage.update_task(
                task.id, 
                title=f"Updated Task {i}", 
                description=f"Updated description for task {i}"
            )
        
        end_time = time.time()
        update_time = end_time - start_time
        
        print(f"Time to update 1000 tasks: {update_time:.2f} seconds")
        
        # Measure time to get all tasks after updates
        start_time = time.time()
        updated_tasks = test_storage.get_all_tasks()
        end_time = time.time()
        get_after_update_time = end_time - start_time
        
        print(f"Time to retrieve 1000 tasks after updates: {get_after_update_time:.2f} seconds")
        
        # Verify all tasks were updated
        assert len(updated_tasks) == 1000, f"Expected 1000 updated tasks, got {len(updated_tasks)}"
        
        # Performance requirements check
        assert add_time < 2.0, f"Adding 1000 tasks took {add_time:.2f}s, which exceeds 2s limit"
        assert get_time < 2.0, f"Retrieving 1000 tasks took {get_time:.2f}s, which exceeds 2s limit"
        assert update_time < 2.0, f"Updating 1000 tasks took {update_time:.2f}s, which exceeds 2s limit"
        assert get_after_update_time < 2.0, f"Retrieving 1000 tasks after updates took {get_after_update_time:.2f}s, which exceeds 2s limit"
        
        print("✅ Performance test passed: All operations completed within 2 seconds for 1000 tasks")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")
        return False
        
    finally:
        # Restore original persistence
        persistence.persistence = original_persistence

        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test_concurrent_access_simulation():
    """
    Test that the storage can handle simulated concurrent access patterns.
    This simulates multiple pods accessing the storage simultaneously.
    """
    print("Testing concurrent access simulation...")
    
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name

    # Create a new storage instance that uses our temporary file
    from src.todo_engine import persistence
    original_file_path = persistence.persistence.file_path
    try:
        # Temporarily replace the persistence instance with our temp file
        original_persistence = persistence.persistence
        persistence.persistence = persistence.FilePersistence(temp_filename)

        # Create a new storage instance with the temporary persistence
        test_storage = FileStorage()
        
        # Add a few initial tasks
        for i in range(5):
            task = create_task(f"Initial Task {i}", f"Initial description for task {i}")
            test_storage.add_task(task)
        
        # Simulate multiple "pods" accessing the storage
        # In a real Kubernetes environment, multiple pods would have separate instances
        # but share the same persistent storage. Here we simulate this by using the same 
        # persistence file with different storage instances.
        
        # Pod 1: Adds a task
        pod1_storage = FileStorage()
        task = create_task("Task from Pod 1", "Added by simulated Pod 1")
        pod1_storage.add_task(task)
        
        # Pod 2: Updates a task
        pod2_storage = FileStorage()
        all_tasks = pod2_storage.get_all_tasks()
        if len(all_tasks) > 0:
            first_task = all_tasks[0]
            updated_task = pod2_storage.update_task(first_task.id, "Updated by Pod 2", "Updated by simulated Pod 2")
        
        # Pod 3: Views all tasks
        pod3_storage = FileStorage()
        tasks = pod3_storage.get_all_tasks()
        
        # Verify the changes from all "pods" are reflected
        assert len(tasks) == 6, f"Expected 6 tasks (5 initial + 1 from Pod 1), got {len(tasks)}"
        
        # Check that the update from Pod 2 is reflected
        updated_task = next((t for t in tasks if t.title == "Updated by Pod 2"), None)
        assert updated_task is not None, "Task updated by Pod 2 was not found"
        
        print("✅ Concurrent access simulation passed: Multiple storage instances correctly interact with shared persistence")
        
        return True
        
    except Exception as e:
        print(f"❌ Concurrent access simulation failed: {str(e)}")
        return False
        
    finally:
        # Restore original persistence
        persistence.persistence = original_persistence

        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


if __name__ == "__main__":
    print("Running performance tests for Phase V: Cloud Deployment & Scaling...\n")
    
    success1 = test_performance_with_1000_tasks()
    print()  # Empty line for readability
    success2 = test_concurrent_access_simulation()
    
    print(f"\nPerformance test results:")
    print(f"- 1000 tasks performance: {'PASS' if success1 else 'FAIL'}")
    print(f"- Concurrent access simulation: {'PASS' if success2 else 'FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All performance tests passed!")
        exit(0)
    else:
        print("\n💥 Some performance tests failed!")
        exit(1)