# Data Model: Web Application & Database Persistence

## Entity: Task

### Fields
- **id** (UUID string)
  - Type: string (UUID format)
  - Constraints: Primary key, required, must be valid UUID
  - Source: Generated on creation

- **title** (Task title)
  - Type: string
  - Constraints: Required, 1-255 characters
  - Validation: Length must be between 1 and 255 characters

- **description** (Task description)
  - Type: string | null
  - Constraints: Optional, max 1000 characters if provided
  - Validation: If provided, length must be between 1 and 1000 characters

- **completed** (Completion status)
  - Type: boolean
  - Constraints: Required, default false
  - Values: true (completed) or false (incomplete)

- **created_at** (Creation timestamp)
  - Type: string (ISO 8601 format) or Date object
  - Constraints: Required, auto-generated on creation
  - Format: YYYY-MM-DDTHH:mm:ss.sssZ

- **updated_at** (Last update timestamp)
  - Type: string (ISO 8601 format) or Date object
  - Constraints: Required, auto-updated on any change
  - Format: YYYY-MM-DDTHH:mm:ss.sssZ

### Relationships
- No relationships with other entities (standalone entity)

### State Transitions
- Creation: `completed` defaults to `false`
- Update: `completed` can toggle between `true` and `false`
- Update: `title` and `description` can be modified
- Update: `updated_at` automatically updates on any change

## Database Schema

### Table: tasks
```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL CHECK (length(title) >= 1 AND length(title) <= 255),
  description TEXT,
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to update updated_at on modification
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = CURRENT_TIMESTAMP;
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tasks_updated_at 
    BEFORE UPDATE ON tasks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

## Validation Rules

### Input Validation
- Title: Required, string type, 1-255 characters
- Description: Optional, string type if provided, max 1000 characters
- ID: Must be valid UUID format when provided as parameter
- Completed: Must be boolean type

### Business Rules
- Task must have a valid UUID as ID
- Task must have a title between 1-255 characters
- Task can optionally have a description up to 1000 characters
- Task completion status is boolean
- Creation and update timestamps are automatically managed