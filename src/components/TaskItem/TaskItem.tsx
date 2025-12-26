'use client';

import { useState } from 'react';
import { Task } from '@/types/task';

interface TaskItemProps {
  task: Task;
  onToggleCompletion: (id: string) => void;
  onUpdateTask: (id: string, title: string, description: string) => void;
  onDeleteTask: (id: string) => void;
}

export default function TaskItem({ task, onToggleCompletion, onUpdateTask, onDeleteTask }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [isConfirmingDelete, setIsConfirmingDelete] = useState(false);

  const handleSave = () => {
    onUpdateTask(task.id, title, description);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (isConfirmingDelete) {
      onDeleteTask(task.id);
    } else {
      setIsConfirmingDelete(true);
      // Reset confirmation after 5 seconds
      setTimeout(() => setIsConfirmingDelete(false), 5000);
    }
  };

  return (
    <div className={`todo-task-item ${task.completed ? 'todo-task-item.completed' : ''}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="todo-input-edit"
            maxLength={255}
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="todo-input-edit"
            maxLength={1000}
            rows={2}
          />
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              className="todo-task-action-btn todo-button-success"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="todo-task-action-btn todo-button-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleCompletion(task.id)}
              className="todo-checkbox mt-1 mr-2"
            />
            <div className="flex-1">
              <h3 className={`todo-task-title ${task.completed ? 'todo-task-title.completed' : ''}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`todo-task-description ${task.completed ? 'todo-task-description.completed' : ''}`}>
                  {task.description}
                </p>
              )}
              <p className="todo-task-meta">
                Created: {new Date(task.created_at).toLocaleString()}
                {task.updated_at !== task.created_at && ` | Updated: ${new Date(task.updated_at).toLocaleString()}`}
              </p>
            </div>
          </div>

          <div className="todo-task-actions">
            <button
              onClick={() => setIsEditing(true)}
              className="todo-task-action-btn todo-button-warning"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className={`todo-task-action-btn ${isConfirmingDelete ? 'todo-button-danger' : 'todo-button-danger'}`}
            >
              {isConfirmingDelete ? 'Confirm Delete' : 'Delete'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}