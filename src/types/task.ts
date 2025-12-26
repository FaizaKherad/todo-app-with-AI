export interface Task {
  id: string; // UUID string
  title: string; // 1-255 characters
  description: string | null; // Optional, max 1000 characters
  completed: boolean;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

export interface TaskInput {
  title: string; // 1-255 characters
  description?: string | null; // Optional, max 1000 characters
}