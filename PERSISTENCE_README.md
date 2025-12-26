# Core Todo Engine - Phase II: Persistence & Validation

## Overview

This is Phase II of the Todo Evolution Project, which extends the Core Todo Engine by introducing persistent storage, enhanced validation rules, and deterministic error handling. All functionality from Phase I remains unchanged.

## Features

### Persistent Storage
- Tasks are now saved to `tasks.json` file automatically
- All changes (add, update, delete, complete) are persisted to disk
- Tasks survive application restarts

### Enhanced Validation
- Title: 1-255 characters (increased from 1-100 in Phase I)
- Description: 0-1000 characters (increased from 0-500 in Phase I)
- Task ID: Valid UUID v4 format required

### Error Handling
- All errors now return in a consistent JSON format:
  ```json
  {
    "error_code": "ERROR_CODE",
    "message": "Human-readable explanation"
  }
  ```

## Usage

### Add a Task
```bash
python main.py add --title "Task title" --description "Task description"
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

### Toggle Task Completion
```bash
python main.py complete --id <task-id>
```

## Error Codes

- `TASK_NOT_FOUND`: Task with the given ID does not exist
- `INVALID_TITLE`: Title validation failed (empty, too long, etc.)
- `PERSISTENCE_WRITE_FAILED`: Failed to save tasks to file
- `UNKNOWN_ERROR`: Other error occurred

## Architecture

- `src/todo_engine/persistence.py`: File-based persistence logic
- `src/todo_engine/storage.py`: Storage layer with persistence integration
- `src/todo_engine/models.py`: Task model with enhanced validation
- `src/todo_engine/cli.py`: CLI with updated error handling

## Testing

Run the test suite:
```bash
pytest
```

The test suite includes:
- Unit tests for persistence functionality
- Validation tests
- Integration tests for file operations