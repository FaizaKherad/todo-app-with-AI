import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json();

    if (!message || typeof message !== 'string') {
      return Response.json(
        { error: 'Message is required and must be a string' },
        { status: 400 }
      );
    }

    // For a completely free solution without API keys, we'll use a more sophisticated mock response
    // that simulates AI-like behavior for common todo app queries
    const aiResponse = getAdvancedMockResponse(message);

    return Response.json({
      success: true,
      response: aiResponse,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error in AI chat API:', error);
    return Response.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to process AI request',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

// Advanced mock response generator that simulates AI-like behavior
function getAdvancedMockResponse(userMessage: string): string {
  const lowerCaseMessage = userMessage.toLowerCase();

  // Greetings
  if (lowerCaseMessage.includes('hello') || lowerCaseMessage.includes('hi') || lowerCaseMessage.includes('hey')) {
    return "Hello! I'm your AI assistant for the Todo app. How can I help you manage your tasks today?";
  }

  // Questions about adding tasks
  if (lowerCaseMessage.includes('add') || lowerCaseMessage.includes('create') || lowerCaseMessage.includes('new task')) {
    return "To add a new task, simply type in the task title in the input field above and click 'Add Task'. You can also add an optional description. The task will appear in your list immediately!";
  }

  // Questions about completing tasks
  if (lowerCaseMessage.includes('complete') || lowerCaseMessage.includes('done') || lowerCaseMessage.includes('finish') || lowerCaseMessage.includes('mark as')) {
    return "To mark a task as complete, just click the checkbox next to the task in your list. The task will be visually marked as completed and you'll see a strikethrough on the title.";
  }

  // Questions about deleting tasks
  if (lowerCaseMessage.includes('delete') || lowerCaseMessage.includes('remove') || lowerCaseMessage.includes('erase')) {
    return "To delete a task, click the 'Delete' button on the task item. You'll need to confirm the deletion to prevent accidental removal of tasks.";
  }

  // Questions about editing tasks
  if (lowerCaseMessage.includes('edit') || lowerCaseMessage.includes('update') || lowerCaseMessage.includes('change')) {
    return "To edit a task, click the 'Edit' button on the task item. This will allow you to modify the title and description. After making your changes, click 'Save' to update the task.";
  }

  // Questions about help or commands
  if (lowerCaseMessage.includes('help') || lowerCaseMessage.includes('command') || lowerCaseMessage.includes('what can you do')) {
    return "I can help you with managing your tasks! You can ask me about adding tasks, completing tasks, editing tasks, or deleting tasks. For example, you can say 'How do I add a task?' or 'Tell me about editing tasks.'";
  }

  // Thank you responses
  if (lowerCaseMessage.includes('thank')) {
    return "You're welcome! Feel free to ask if you need help with anything else related to your tasks.";
  }

  // Questions about features
  if (lowerCaseMessage.includes('feature') || lowerCaseMessage.includes('can i') || lowerCaseMessage.includes('able to')) {
    return "Our Todo app allows you to create, read, update, and delete tasks. You can mark tasks as complete, edit task details, and organize your productivity. The AI assistant is here to help you navigate these features!";
  }

  // Default response that acknowledges the input
  return `I understand you're asking about "${userMessage}". I'm your AI assistant for the Todo app. You can ask me how to add, complete, edit, or delete tasks. For example, you could ask: "How do I add a new task?" or "Show me how to mark tasks as complete."`;
}