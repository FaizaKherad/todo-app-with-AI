import { NextRequest } from 'next/server';
import { toggleTaskCompletion } from '@/lib/tasks';

// Handler for PATCH requests to /api/tasks/[id]/complete
export async function PATCH(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const id = params.id;
    console.log('PATCH request received for task ID:', id);

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

    const toggledTask = await toggleTaskCompletion(id);
    console.log('Toggle completion result:', toggledTask);

    if (!toggledTask) {
      console.log('Task not found for completion toggle:', id);
      return Response.json(
        {
          error_code: 'TASK_NOT_FOUND',
          message: 'Task with provided ID not found'
        },
        { status: 404 }
      );
    }

    console.log('Task completion toggled successfully:', id);
    return Response.json({ data: toggledTask });
  } catch (error) {
    console.error('Error toggling task completion:', error);
    return Response.json(
      {
        error_code: 'SERVER_ERROR',
        message: 'Failed to update task completion status: ' + (error instanceof Error ? error.message : 'Unknown error')
      },
      { status: 500 }
    );
  }
}