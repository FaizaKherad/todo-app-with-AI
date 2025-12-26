# Core Todo Engine - Phase III: Conversational AI Interface

## Overview

This is Phase III of the Todo Evolution Project, which adds a conversational AI interface to the Core Todo Engine. The system now accepts natural language commands to manage your todo list, while maintaining all the functionality from previous phases.

## Features

### Conversational Interface
- Natural language commands for all todo operations
- AI-powered intent recognition and parameter extraction
- Human-like responses with appropriate feedback

### Supported Commands

#### Creating Tasks
- "Add a task to buy groceries"
- "Create a todo called submit report"
- "Make a new task to clean the house"

#### Viewing Tasks
- "Show my tasks"
- "What do I need to do?"
- "List all my todos"

#### Updating Tasks
- "Rename my grocery task to buy vegetables"
- "Update the report task description to include budget figures"

#### Deleting Tasks
- "Delete the grocery task"
- "Remove task submit report"

#### Completing Tasks
- "Mark groceries as done"
- "Complete my report task"

## Usage

### Interactive Mode
Run the application without arguments to start the conversational interface:

```bash
python main.py
```

Then simply type your commands in natural language.

### Command Mode
Continue to use the command-line interface as before:

```bash
python main.py add --title "Task title" --description "Task description"
python main.py list
python main.py update --id <task-id> --title "New title"
python main.py delete --id <task-id>
python main.py complete --id <task-id>
```

### AI Mode from CLI
You can also access the AI interface from the command line:

```bash
python main.py ai --prompt "Add a task to buy groceries"
```

## Architecture

- `src/todo_engine/ai_assistant.py`: AI assistant that interprets natural language
- `src/todo_engine/mcp_tools.py`: MCP tools that interface with the core engine
- `src/todo_engine/ai/`: Directory for AI-related modules
- All existing functionality from Phases I & II preserved

## Configuration

The system can be configured via environment variables:

- `OPENAI_API_KEY`: API key for OpenAI integration (optional)
- `AI_MODEL`: Model to use for AI assistant (default: gpt-3.5-turbo)
- `AI_TEMPERATURE`: Creativity setting for AI responses (default: 0.7)
- `MCP_ENABLED`: Enable MCP tools (default: true)

## Error Handling

The system provides human-readable error messages when:
- Tasks are not found
- Validation rules are violated
- Ambiguous requests are made
- API connectivity issues occur

## Integration

The AI assistant acts as an orchestration layer that:
- Interprets natural language commands
- Routes actions to the appropriate core functions
- Formats responses for human readability
- Preserves all validation and business logic from previous phases