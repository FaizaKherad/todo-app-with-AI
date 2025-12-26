from src.todo_engine.mcp_tools import MCPTaskTools
import tempfile
import os

# Create a temporary file for testing
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
    temp_filename = temp_file.name

# Create tools with the temp file
from src.todo_engine import persistence
original_persistence = persistence.persistence
persistence.persistence = persistence.FilePersistence(temp_filename)

# Create a fresh storage instance
from src.todo_engine import storage
from src.todo_engine.storage import FileStorage
original_storage = storage.storage
storage.storage = FileStorage()  # This will load from the empty temp file

# Now test
tools = MCPTaskTools()
print('Initial tasks:', len(tools.view_tasks()))

# Add a task
result = tools.add_task('Test task', 'Test description')
print('Added task:', result['title'])

# View tasks
tasks = tools.view_tasks()
print('Tasks after adding:', len(tasks))

# Clean up
persistence.persistence = original_persistence
storage.storage = original_storage
if os.path.exists(temp_filename):
    os.remove(temp_filename)

print('Test completed successfully')