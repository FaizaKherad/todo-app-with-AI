# API Contract: Todo Application

## Overview
This document specifies the API contracts for the Todo application. All endpoints follow RESTful patterns and return JSON responses.

## Base URL
`http://localhost:3000/api` (development)
`https://[deployed-domain]/api` (production)

## Common Response Format

### Success Response
```json
{
  "data": { /* response data */ }
}
```

### Error Response
```json
{
  "error_code": "STRING",
  "message": "Human-readable explanation"
}
```

## Endpoints

### GET /tasks
**Description**: Retrieve all tasks from the database

**Request**:
- Method: GET
- Path: /api/tasks
- Headers: None required
- Query Parameters: None

**Response**:
- Success (200): Array of Task objects
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Sample task",
      "description": "Sample description",
      "completed": false,
      "created_at": "2025-12-25T10:00:00.000Z",
      "updated_at": "2025-12-25T10:00:00.000Z"
    }
  ]
}
```
- Error (500): Server error
```json
{
  "error_code": "SERVER_ERROR",
  "message": "Failed to retrieve tasks"
}
```

### POST /tasks
**Description**: Create a new task

**Request**:
- Method: POST
- Path: /api/tasks
- Headers: 
  - Content-Type: application/json
- Body:
```json
{
  "title": "Task title (required, 1-255 chars)",
  "description": "Task description (optional, max 1000 chars)"
}
```

**Response**:
- Success (201): Created Task object
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2025-12-25T10:00:00.000Z",
    "updated_at": "2025-12-25T10:00:00.000Z"
  }
}
```
- Error (400): Validation error
```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Title is required and must be 1-255 characters"
}
```
- Error (500): Server error
```json
{
  "error_code": "SERVER_ERROR",
  "message": "Failed to create task"
}
```

### PUT /tasks/{id}
**Description**: Update an existing task

**Request**:
- Method: PUT
- Path: /api/tasks/{id}
- Headers: 
  - Content-Type: application/json
- Path Parameter: id (valid UUID)
- Body:
```json
{
  "title": "Updated task title (required, 1-255 chars)",
  "description": "Updated task description (optional, max 1000 chars)"
}
```

**Response**:
- Success (200): Updated Task object
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false,
    "created_at": "2025-12-25T10:00:00.000Z",
    "updated_at": "2025-12-25T11:00:00.000Z"
  }
}
```
- Error (400): Validation error
```json
{
  "error_code": "VALIDATION_ERROR",
  "message": "Title is required and must be 1-255 characters"
}
```
- Error (404): Task not found
```json
{
  "error_code": "TASK_NOT_FOUND",
  "message": "Task with provided ID not found"
}
```
- Error (500): Server error
```json
{
  "error_code": "SERVER_ERROR",
  "message": "Failed to update task"
}
```

### DELETE /tasks/{id}
**Description**: Delete a task

**Request**:
- Method: DELETE
- Path: /api/tasks/{id}
- Path Parameter: id (valid UUID)

**Response**:
- Success (200): Deletion confirmation
```json
{
  "data": {
    "success": true,
    "message": "Task deleted successfully"
  }
}
```
- Error (404): Task not found
```json
{
  "error_code": "TASK_NOT_FOUND",
  "message": "Task with provided ID not found"
}
```
- Error (500): Server error
```json
{
  "error_code": "SERVER_ERROR",
  "message": "Failed to delete task"
}
```

### PATCH /tasks/{id}/complete
**Description**: Toggle task completion status

**Request**:
- Method: PATCH
- Path: /api/tasks/{id}/complete
- Path Parameter: id (valid UUID)

**Response**:
- Success (200): Updated Task object
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "created_at": "2025-12-25T10:00:00.000Z",
    "updated_at": "2025-12-25T11:00:00.000Z"
  }
}
```
- Error (404): Task not found
```json
{
  "error_code": "TASK_NOT_FOUND",
  "message": "Task with provided ID not found"
}
```
- Error (500): Server error
```json
{
  "error_code": "SERVER_ERROR",
  "message": "Failed to update task completion status"
}
```

## Data Models

### Task
```json
{
  "id": "string (UUID)",
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters) or null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```