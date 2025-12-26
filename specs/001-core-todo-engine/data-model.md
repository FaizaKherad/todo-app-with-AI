# Data Model: Core Todo Engine

**Feature**: Core Todo Engine (Phase I)
**Date**: 2025-12-24

## Overview

This document defines the data model for the Core Todo Engine, detailing the structure of the Task entity and its relationships as specified in the feature requirements.

## Task Entity

### Structure

The Task entity represents a single todo item with the following fields:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| id | string (UUID v4) | Yes | Must be valid UUID v4 format | Unique identifier for the task |
| title | string | Yes | 1-100 characters, non-empty | Short task title |
| description | string | No | 0-500 characters | Optional task details |
| completed | boolean | Yes | Must be true or false | Completion status |
| created_at | string (ISO 8601) | Yes | Valid ISO 8601 timestamp | Timestamp when task was created |
| updated_at | string (ISO 8601) | Yes | Valid ISO 8601 timestamp | Timestamp when task was last updated |

### Example

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the Core Todo Engine",
  "completed": false,
  "created_at": "2025-12-24T10:30:00Z",
  "updated_at": "2025-12-24T10:30:00Z"
}
```

## State Transitions

The Task entity has a single state attribute (completed) that can transition as follows:

- **Incomplete** (completed: false) → **Complete** (completed: true) when marked as complete
- **Complete** (completed: true) → **Incomplete** (completed: false) when marked as incomplete

## Validation Rules

1. **ID Validation**: Must be a valid UUID v4 string
2. **Title Validation**: 
   - Required field
   - Minimum 1 character
   - Maximum 100 characters
   - Cannot be empty or whitespace-only
3. **Description Validation**:
   - Optional field
   - Maximum 500 characters
4. **Completion Validation**:
   - Must be a boolean value (true or false)
5. **Timestamp Validation**:
   - Must be in ISO 8601 format
   - created_at and updated_at must be valid timestamps

## Data Storage

Tasks are stored in-memory only for Phase I:
- Storage mechanism: Python dictionary with UUID as key
- Persistence: None (data lost when application stops)
- Concurrency: Single-threaded access (no concurrent modifications)

## Business Rules

1. New tasks must be created with completed = false by default
2. New tasks must have both created_at and updated_at set to the current timestamp
3. When updating a task, only the updated_at timestamp should be modified
4. When toggling completion status, only the completed field and updated_at timestamp should be modified
5. Task IDs are immutable once created