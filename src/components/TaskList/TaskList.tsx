'use client';

import { useEffect, useState } from 'react';
import TaskItem from '../TaskItem/TaskItem';
import { Task } from '@/types/task';

interface TaskListProps {
  initialTasks?: Task[];
}

export default function TaskList({ initialTasks = [] }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/tasks');
      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }
      const { data } = await response.json();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError('Failed to load tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleCompletion = async (id: string) => {
    try {
      const response = await fetch(`/api/tasks/${id}/complete`, {
        method: 'PATCH',
      });

      if (!response.ok) {
        const { message } = await response.json();
        throw new Error(message);
      }

      const { data: updatedTask } = await response.json();
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      console.error('Error toggling task completion:', err);
      alert('Failed to update task completion status');
    }
  };

  const handleUpdateTask = async (id: string, title: string, description: string) => {
    try {
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description }),
      });

      if (!response.ok) {
        const { message } = await response.json();
        throw new Error(message);
      }

      const { data: updatedTask } = await response.json();
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (err) {
      console.error('Error updating task:', err);
      alert('Failed to update task');
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      const response = await fetch(`/api/tasks/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const { message } = await response.json();
        throw new Error(message);
      }

      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      console.error('Error deleting task:', err);
      alert('Failed to delete task');
    }
  };

  if (loading) {
    return <div className="todo-loading">Loading tasks...</div>;
  }

  if (error) {
    return <div className="todo-error-message">{error}</div>;
  }

  if (tasks.length === 0) {
    return (
      <div className="todo-empty-state">
        <h3 className="todo-empty-title">No tasks yet</h3>
        <p className="todo-empty-message">Add a new task to get started!</p>
      </div>
    );
  }

  return (
    <div className="todo-task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleCompletion={handleToggleCompletion}
          onUpdateTask={handleUpdateTask}
          onDeleteTask={handleDeleteTask}
        />
      ))}
    </div>
  );
}