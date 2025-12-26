# Quickstart Guide: Core Todo Engine

**Feature**: Core Todo Engine (Phase I)
**Date**: 2025-12-24

## Overview

This guide provides instructions to quickly set up and run the Core Todo Engine CLI application. The application allows users to manage tasks through a command-line interface with full CRUD functionality.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Setup

1. **Clone or access the repository**
   ```bash
   # If using a repository
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if no requirements.txt exists yet:
   ```bash
   pip install argparse pytest
   ```

## Running the Application

To run the Core Todo Engine CLI application:

```bash
python main.py --help
```

This will display the available commands and their usage.

## Available Commands

### Add a Task
```bash
python main.py add --title "Task title" --description "Optional description"
```

### List All Tasks
```bash
python main.py list
```

### Update a Task
```bash
python main.py update --id <task-id> --title "New title" --description "New description"
```

### Delete a Task
```bash
python main.py delete --id <task-id>
```

### Mark Task as Complete/Incomplete
```bash
python main.py complete --id <task-id>
```

## Example Usage

```bash
# Add a new task
python main.py add --title "Complete project" --description "Implement all required features"

# List all tasks
python main.py list

# Update a task (replace <task-id> with actual ID from list)
python main.py update --id 550e8400-e29b-41d4-a716-446655440000 --title "Complete Phase I"

# Mark a task as complete
python main.py complete --id 550e8400-e29b-41d4-a716-446655440000

# Delete a task
python main.py delete --id 550e8400-e29b-41d4-a716-446655440000
```

## Configuration

The application can be configured through a config.py file:

```python
# Configuration settings
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "todo_app.log"  # Set to None to disable file logging
```

## Running Tests

To run the test suite:

```bash
pytest
```

Or for more verbose output:

```bash
pytest -v
```

## Architecture Overview

The application is structured as follows:

- `main.py` - Entry point of the application
- `src/todo_engine/cli.py` - Command-line interface logic
- `src/todo_engine/models.py` - Task data model
- `src/todo_engine/storage.py` - In-memory storage implementation
- `src/todo_engine/logger.py` - Logging utilities
- `tests/` - Unit and integration tests

## Troubleshooting

### Common Issues

1. **Command not found**: Make sure you're running the command from the correct directory where main.py is located.

2. **Python version error**: Ensure you're using Python 3.11 or higher.

3. **Permission error**: On Unix systems, ensure you have the necessary permissions to execute the Python files.

## Next Steps

After successfully running the Core Todo Engine:

1. Explore the codebase to understand the implementation
2. Run the test suite to ensure everything works correctly
3. Implement the tasks defined in tasks.md
4. Consider extending functionality in future phases (persistence, web interface, etc.)