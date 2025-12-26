'use client';

import { useState } from 'react';
import { Task } from '@/types/task';

interface TaskFormProps {
  onTaskAdded: (task: Task) => void;
}

export default function TaskForm({ onTaskAdded }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.length > 255) {
      setError('Title must be 255 characters or less');
      return;
    }

    if (description && description.length > 1000) {
      setError('Description must be 1000 characters or less');
      return;
    }

    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch('/api/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description: description || null }),
      });

      if (!response.ok) {
        const { message } = await response.json();
        throw new Error(message);
      }

      const { data: newTask } = await response.json();
      onTaskAdded(newTask);

      // Reset form
      setTitle('');
      setDescription('');
    } catch (err) {
      console.error('Error creating task:', err);
      setError('Failed to create task');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <div className="mb-4">
        <label htmlFor="title" className="todo-label">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="todo-input"
          placeholder="Enter task title (1-255 characters)"
          maxLength={255}
          required
        />
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="todo-label">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="todo-input"
          placeholder="Enter task description (optional, max 1000 characters)"
          maxLength={1000}
          rows={3}
        />
      </div>

      {error && (
        <div className="todo-error-message">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className={`todo-button ${isLoading ? 'bg-gray-400 cursor-not-allowed' : 'todo-button-primary'}`}
      >
        {isLoading ? 'Adding Task...' : 'Add Task'}
      </button>
    </form>
  );
}