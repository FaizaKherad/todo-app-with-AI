import { NextRequest } from 'next/server';
import { updateTask, deleteTask, getTaskById } from '@/lib/tasks';
import { TaskInput } from '@/types/task';

// Handler for PUT and DELETE requests to /api/tasks/[id]
export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const id = params.id;
    console.log('PUT request received for task ID:', id);

    // Validate UUID format
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(id)) {
      console.log('Invalid UUID format:', id);
      return Response.json(
        {
          error_code: 'VALIDATION_ERROR',
          message: 'Invalid task ID format'
        },
        { status: 400 }
      );
    }

    const body: TaskInput = await request.json();
    console.log('PUT request body:', body);

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

    const updatedTask = await updateTask(id, body);
    console.log('Update operation result:', updatedTask);

    if (!updatedTask) {
      console.log('Task not found for update:', id);
      return Response.json(
        {
          error_code: 'TASK_NOT_FOUND',
          message: 'Task with provided ID not found'
        },
        { status: 404 }
      );
    }

    console.log('Task updated successfully:', id);
    return Response.json({ data: updatedTask });
  } catch (error) {
    console.error('Error updating task:', error);
    return Response.json(
      {
        error_code: 'SERVER_ERROR',
        message: 'Failed to update task: ' + (error instanceof Error ? error.message : 'Unknown error')
      },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const id = params.id;

    console.log('DELETE request received for task ID:', id);

    // Validate UUID format
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(id)) {
      console.log('Invalid UUID format:', id);
      return Response.json(
        {
          error_code: 'VALIDATION_ERROR',
          message: 'Invalid task ID format'
        },
        { status: 400 }
      );
    }

    const success = await deleteTask(id);
    console.log('Delete operation result:', success);

    if (!success) {
      console.log('Task not found for deletion:', id);
      return Response.json(
        {
          error_code: 'TASK_NOT_FOUND',
          message: 'Task with provided ID not found'
        },
        { status: 404 }
      );
    }

    console.log('Task deleted successfully:', id);
    return Response.json({
      data: {
        success: true,
        message: 'Task deleted successfully'
      }
    });
  } catch (error) {
    console.error('Error deleting task:', error);
    return Response.json(
      {
        error_code: 'SERVER_ERROR',
        message: 'Failed to delete task: ' + (error instanceof Error ? error.message : 'Unknown error')
      },
      { status: 500 }
    );
  }
}