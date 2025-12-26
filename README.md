# Web Todo Application

A full-stack Next.js application with Tailwind CSS styling and NeonDB (PostgreSQL) persistence. The solution provides a browser-based UI that exposes all todo capabilities (view, add, update, delete, complete) through HTTP API endpoints that interact with the PostgreSQL database. Includes an AI-powered chatbot assistant for task management.

## Features

- View all tasks with clear completion status
- Add new tasks with title and optional description
- Update existing tasks
- Delete tasks with confirmation
- Toggle task completion status
- Responsive UI that works on all screen sizes
- Input validation for all operations
- Error handling and user feedback
- AI-powered chatbot assistant for task management

## Tech Stack

- Next.js 14+ (App Router)
- React
- TypeScript
- Tailwind CSS
- NeonDB (PostgreSQL)
- Node.js

## Prerequisites

- Node.js 18+
- npm or yarn package manager
- NeonDB account and database URL

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Configure environment variables:
   Create a `.env.local` file in the project root with your NeonDB connection string:
   ```
   DATABASE_URL=your_neon_db_connection_string_here
   ```

   Note: The AI chatbot uses a sophisticated mock response system that simulates AI behavior without requiring external API keys, making it completely free to use.

4. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The application will be available at `http://localhost:3000`

## API Endpoints

- `GET /api/tasks` - Retrieve all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update an existing task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status
- `POST /api/ai-chat` - Interact with the AI assistant

## AI Chatbot Capabilities

The application includes an AI-powered chatbot that can help you with:
- Adding tasks to your list
- Marking tasks as complete
- Deleting tasks
- Editing existing tasks
- General questions about the application

To use the chatbot, click the floating chat icon in the bottom right corner of the screen.

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── api/             # API routes for todo operations
│   │   ├── tasks/
│   │   │   ├── route.ts    # Handles GET, POST for all tasks
│   │   │   └── [id]/
│   │   │       ├── route.ts    # Handles PUT, DELETE for specific task
│   │   │       └── complete/
│   │   │           └── route.ts    # Handles PATCH for completion toggle
│   │   └── ai-chat/         # AI chatbot API route
│   │       └── route.ts      # Handles AI chat interactions
│   ├── components/      # React components
│   │   ├── TaskList/
│   │   ├── TaskForm/
│   │   ├── TaskItem/
│   │   └── AIChatBot/       # AI chatbot component
│   │       └── AIChatBot.tsx # AI chat interface
│   ├── lib/             # Utility functions and database connection
│   │   ├── db.ts        # Database connection and initialization
│   │   └── tasks.ts     # Task data access functions
│   └── types/           # TypeScript type definitions
│       └── task.ts      # Task interface/type definition
└── styles/              # Global styles
    └── globals.css      # Tailwind CSS configuration
```

## Database Schema

The application uses a single `tasks` table with the following structure:
- `id`: UUID primary key
- `title`: TEXT, NOT NULL (1-255 characters)
- `description`: TEXT, NULL (max 1000 characters)
- `completed`: BOOLEAN, NOT NULL, DEFAULT FALSE
- `created_at`: TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP