import { pool } from './db';
import { Task, TaskInput } from '../types/task';

// Get all tasks from the database
export const getAllTasks = async (): Promise<Task[]> => {
  try {
    const result = await pool.query('SELECT * FROM tasks ORDER BY created_at DESC');
    return result.rows as Task[];
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

// Create a new task in the database
export const createTask = async (taskInput: TaskInput): Promise<Task> => {
  try {
    const { title, description } = taskInput;

    // Validate title length
    if (!title || title.length < 1 || title.length > 255) {
      throw new Error('Title is required and must be 1-255 characters');
    }

    // Validate description length if provided
    if (description && description.length > 1000) {
      throw new Error('Description must be 1000 characters or less');
    }

    const result = await pool.query(
      'INSERT INTO tasks (title, description, completed) VALUES ($1, $2, $3) RETURNING *',
      [title, description || null, false]
    );

    return result.rows[0] as Task;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

// Update an existing task in the database
export const updateTask = async (id: string, taskInput: TaskInput): Promise<Task | null> => {
  try {
    console.log('Attempting to update task with ID:', id);
    const { title, description } = taskInput;

    // Validate title length
    if (!title || title.length < 1 || title.length > 255) {
      throw new Error('Title is required and must be 1-255 characters');
    }

    // Validate description length if provided
    if (description && description.length > 1000) {
      throw new Error('Description must be 1000 characters or less');
    }

    const result = await pool.query(
      'UPDATE tasks SET title = $1, description = $2 WHERE id = $3 RETURNING *',
      [title, description || null, id]
    );

    console.log('Update result:', result);
    if (result.rows.length === 0) {
      console.log('No task found with the provided ID:', id);
      return null; // Task not found
    }

    return result.rows[0] as Task;
  } catch (error) {
    console.error('Error updating task:', error);
    // If it's a validation error, re-throw it as is
    if (error instanceof Error && error.message.includes('must be')) {
      throw error;
    }
    // For other errors (like DB connection issues), provide more context
    if (error instanceof Error) {
      throw new Error(`Database error updating task: ${error.message}`);
    } else {
      throw new Error(`Database error updating task: ${(error as Error).message || 'Unknown error'}`);
    }
  }
};

// Delete a task from the database
export const deleteTask = async (id: string): Promise<boolean> => {
  try {
    console.log('Attempting to delete task with ID:', id);
    const result = await pool.query('DELETE FROM tasks WHERE id = $1', [id]);
    console.log('Delete result:', result);

    const deleted = result.rowCount !== 0; // Returns true if a row was deleted
    console.log('Task deleted successfully:', deleted);
    return deleted;
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
};

// Toggle task completion status
export const toggleTaskCompletion = async (id: string): Promise<Task | null> => {
  try {
    console.log('Attempting to toggle completion for task with ID:', id);
    const result = await pool.query(
      'UPDATE tasks SET completed = NOT completed WHERE id = $1 RETURNING *',
      [id]
    );

    console.log('Toggle completion result:', result);
    if (result.rows.length === 0) {
      console.log('No task found with the provided ID for completion toggle:', id);
      return null; // Task not found
    }

    return result.rows[0] as Task;
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
};

// Get a specific task by ID
export const getTaskById = async (id: string): Promise<Task | null> => {
  try {
    const result = await pool.query('SELECT * FROM tasks WHERE id = $1', [id]);

    if (result.rows.length === 0) {
      return null; // Task not found
    }

    return result.rows[0] as Task;
  } catch (error) {
    console.error('Error fetching task by ID:', error);
    throw error;
  }
};