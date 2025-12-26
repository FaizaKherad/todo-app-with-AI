# Quickstart Guide: Web Application & Database Persistence

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- NeonDB account and database URL
- Git for version control

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [repository-url]
cd [repository-name]
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables
Create a `.env.local` file in the project root with your NeonDB connection string:
```env
DATABASE_URL=your_neon_db_connection_string_here
```

### 4. Initialize the Database
The application will automatically create the required schema on first run. No manual setup required.

### 5. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## API Endpoints

### Available Endpoints
- `GET /api/tasks` - Retrieve all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update an existing task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

### Example API Usage

#### Create a Task
```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My new task", "description": "A sample task"}'
```

#### Get All Tasks
```bash
curl http://localhost:3000/api/tasks
```

## Project Structure
```
src/
├── app/                 # Next.js App Router pages
│   ├── api/             # API routes for todo operations
│   ├── components/      # React components
│   ├── lib/             # Utility functions and database connection
│   └── types/           # TypeScript type definitions
└── styles/              # Global styles
```

## Database Schema
The application uses a single `tasks` table with the following structure:
- `id`: UUID primary key
- `title`: TEXT, NOT NULL (1-255 characters)
- `description`: TEXT, NULL (max 1000 characters)
- `completed`: BOOLEAN, NOT NULL, DEFAULT FALSE
- `created_at`: TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP
- `updated_at`: TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP

## Troubleshooting

### Common Issues
- **Database connection errors**: Verify your `DATABASE_URL` environment variable
- **API routes not working**: Check that Next.js is running and the API route files exist
- **UI not loading**: Ensure all dependencies are installed and the development server is running

### Database Initialization
On first run, the application will automatically:
1. Connect to your NeonDB instance
2. Check if the `tasks` table exists
3. Create the table if it doesn't exist
4. Set up necessary triggers for automatic timestamp updates