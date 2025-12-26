# Data Model: Local Cloud-Native Deployment (Minikube)

## Overview

The data model for Phase IV remains unchanged from Phase II, as specified in the feature requirements. The Task entity continues to represent a single todo item with the same fields and validation rules.

## Task Entity

### Structure

The Task entity represents a single todo item with the following fields:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| id | string (UUID v4) | Yes | Valid UUID v4 format | Unique identifier for the task |
| title | string | Yes | 1-255 characters | Short task title |
| description | string | No | 0-1000 characters | Optional task details |
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
   - Maximum 255 characters
   - Cannot be empty or whitespace-only
3. **Description Validation**:
   - Optional field
   - Maximum 1000 characters
4. **Completion Validation**:
   - Must be a boolean value (true or false)
5. **Timestamp Validation**:
   - Must be in ISO 8601 format
   - created_at and updated_at must be valid timestamps

## Storage Model

With the introduction of persistent storage in Phase II and continued in Phase IV, tasks are stored in a JSON file (`tasks.json`) that is mounted to the container via a PersistentVolumeClaim. The storage mechanism remains the same as Phase II but is now containerized and deployed to Kubernetes.

### Persistence

- Location: `/app/data/tasks.json` (inside container, backed by PVC)
- Format: JSON array of Task objects
- Access: File-based read/write operations
- Atomicity: All writes are atomic to prevent data corruption
- Durability: Tasks persist across pod restarts due to PVC backing