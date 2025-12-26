import { NextRequest } from 'next/server';
import { getAllTasks, createTask } from '@/lib/tasks';
import { TaskInput } from '@/types/task';

// Handler for GET and POST requests to /api/tasks
export async function GET(request: NextRequest) {
  try {
    const tasks = await getAllTasks();
    return Response.json({ data: tasks });
  } catch (error) {
    console.error('Error retrieving tasks:', error);
    return Response.json(
      {
        error_code: 'SERVER_ERROR',
        message: 'Failed to retrieve tasks'
      },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body: TaskInput = await request.json();

    // Validate title
    if (!body.title || body.title.length < 1 || body.title.length > 255) {
      return Response.json(
        {
          error_code: 'VALIDATION_ERROR',
          message: 'Title is required and must be 1-255 characters'
        },
        { status: 400 }
      );
    }

    // Validate description if provided
    if (body.description && body.description.length > 1000) {
      return Response.json(
        {
          error_code: 'VALIDATION_ERROR',
          message: 'Description must be 1000 characters or less'
        },
        { status: 400 }
      );
    }

    const newTask = await createTask(body);
    return Response.json({ data: newTask }, { status: 201 });
  } catch (error) {
    console.error('Error creating task:', error);
    return Response.json(
      {
        error_code: 'SERVER_ERROR',
        message: 'Failed to create task'
      },
      { status: 500 }
    );
  }
}