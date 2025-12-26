# CLI Contract: Core Todo Engine

**Feature**: Core Todo Engine (Phase I)
**Date**: 2025-12-24
**Version**: 1.0

## Overview

This document defines the command-line interface (CLI) contract for the Core Todo Engine. It specifies the commands, parameters, and expected behaviors for all user interactions with the application.

## Command Structure

The CLI follows the pattern:
```
python main.py <command> [options]
```

## Commands

### 1. Add Task

**Command**: `add`
**Purpose**: Create a new task in the todo list

**Parameters**:
- `--title` (required): Task title (string, 1-100 characters)
- `--description` (optional): Task description (string, 0-500 characters)

**Usage**:
```
python main.py add --title "Task title" --description "Optional description"
```

**Success Response**:
- Returns the created task in JSON format
- Includes the generated UUID and timestamps

**Error Responses**:
- `INVALID_TITLE`: If title is empty or exceeds 100 characters
- `MISSING_TITLE`: If title is not provided

**Example**:
```
$ python main.py add --title "Complete documentation" --description "Write all required docs"
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete documentation",
  "description": "Write all required docs",
  "completed": false,
  "created_at": "2025-12-24T10:30:00Z",
  "updated_at": "2025-12-24T10:30:00Z"
}
```

### 2. List Tasks

**Command**: `list`
**Purpose**: Retrieve all tasks in the todo list

**Parameters**: None

**Usage**:
```
python main.py list
```

**Success Response**:
- Returns an array of all tasks in JSON format
- If no tasks exist, returns an empty array

**Error Responses**: None

**Example**:
```
$ python main.py list
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Complete documentation",
    "description": "Write all required docs",
    "completed": false,
    "created_at": "2025-12-24T10:30:00Z",
    "updated_at": "2025-12-24T10:30:00Z"
  }
]
```

### 3. Update Task

**Command**: `update`
**Purpose**: Modify an existing task's details

**Parameters**:
- `--id` (required): Task ID (UUID string)
- `--title` (optional): New task title (string, 1-100 characters)
- `--description` (optional): New task description (string, 0-500 characters)

**Usage**:
```
python main.py update --id <task-id> --title "New title" --description "New description"
```

**Success Response**:
- Returns the updated task in JSON format
- Updates the `updated_at` timestamp

**Error Responses**:
- `TASK_NOT_FOUND`: If the task with the given ID does not exist
- `INVALID_TITLE`: If the new title exceeds 100 characters

**Example**:
```
$ python main.py update --id 550e8400-e29b-41d4-a716-446655440000 --title "Updated task"
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated task",
  "description": "Write all required docs",
  "completed": false,
  "created_at": "2025-12-24T10:30:00Z",
  "updated_at": "2025-12-24T11:00:00Z"
}
```

### 4. Delete Task

**Command**: `delete`
**Purpose**: Remove a task permanently from the todo list

**Parameters**:
- `--id` (required): Task ID (UUID string)

**Usage**:
```
python main.py delete --id <task-id>
```

**Success Response**:
- Returns confirmation message with the deleted task ID

**Error Responses**:
- `TASK_NOT_FOUND`: If the task with the given ID does not exist

**Example**:
```
$ python main.py delete --id 550e8400-e29b-41d4-a716-446655440000
{
  "message": "Task deleted successfully",
  "deleted_task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 5. Mark Task Complete/Incomplete

**Command**: `complete`
**Purpose**: Toggle the completion status of a task

**Parameters**:
- `--id` (required): Task ID (UUID string)

**Usage**:
```
python main.py complete --id <task-id>
```

**Success Response**:
- Returns the task with the updated completion status in JSON format
- Updates the `updated_at` timestamp

**Error Responses**:
- `TASK_NOT_FOUND`: If the task with the given ID does not exist

**Example**:
```
$ python main.py complete --id 550e8400-e29b-41d4-a716-446655440000
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated task",
  "description": "Write all required docs",
  "completed": true,
  "created_at": "2025-12-24T10:30:00Z",
  "updated_at": "2025-12-24T11:15:00Z"
}
```

## Common Error Format

All errors follow the format:
```json
{
  "error": "<error_code>",
  "message": "<human-readable error message>",
  "timestamp": "<ISO 8601 timestamp>"
}
```

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `10`: Task not found
- `11`: Invalid title

## Logging

All CLI operations are logged according to the logging configuration. The log levels are:
- INFO: Successful operations
- ERROR: Failed operations
- DEBUG: Detailed operation information (if enabled)