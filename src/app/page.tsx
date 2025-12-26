'use client';

import { useState, useEffect } from 'react';
import TaskList from '../components/TaskList/TaskList';
import TaskForm from '../components/TaskForm/TaskForm';
import ErrorBoundary from '../components/ErrorBoundary';
import AIChatBot from '../components/AIChatBot/AIChatBot';
import { Task } from '@/types/task';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Initial load would happen in TaskList component
    setIsLoading(false);
  }, []);

  const handleTaskAdded = (newTask: Task) => {
    setTasks([newTask, ...tasks]);
  };

  if (isLoading) {
    return (
      <div className="todo-container">
        <div className="todo-card">
          <h1 className="todo-header">Todo App</h1>
          <div className="todo-loading">Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="todo-container">
      <div className="todo-card">
        <h1 className="todo-header">Todo App</h1>

        <ErrorBoundary>
          <TaskForm onTaskAdded={handleTaskAdded} />

          <div>
            <h2 className="todo-section-title">Your Tasks</h2>
            <TaskList initialTasks={tasks} />
          </div>
        </ErrorBoundary>
      </div>
      <AIChatBot />
    </div>
  );
}