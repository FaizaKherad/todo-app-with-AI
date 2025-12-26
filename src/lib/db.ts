import { Pool } from 'pg';

// Create a connection pool using the PostgreSQL client
const connectionString = process.env.DATABASE_URL;

if (!connectionString) {
  console.warn('DATABASE_URL environment variable is not set. The application will not work without a database.');
}

// Create a connection pool for better performance
let pool: Pool;

if (connectionString) {
  pool = new Pool({
    connectionString,
    max: 20, // Maximum number of clients in the pool
    min: 2,  // Minimum number of clients in the pool
    idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
    connectionTimeoutMillis: 5000, // Return an error after 5 seconds if connection could not be established
  });
} else {
  // Create a mock pool that will throw errors if used without proper configuration
  pool = {
    query: async () => {
      throw new Error('Database not configured. Please set DATABASE_URL environment variable.');
    },
    connect: async () => {
      throw new Error('Database not configured. Please set DATABASE_URL environment variable.');
    },
    end: async () => {},
    on: () => {},
  } as unknown as Pool;
}

export { pool };

// Check and initialize the database schema if needed
export const ensureSchema = async (): Promise<void> => {
  if (!connectionString) {
    throw new Error('DATABASE_URL environment variable is required to initialize the database schema.');
  }

  try {
    // Test the connection first
    await pool.query('SELECT 1');

    // Check if the tasks table exists
    const result = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = 'tasks'
      );
    `);

    const tableExists = result.rows[0].exists;

    if (!tableExists) {
      console.log('Tasks table does not exist, creating it...');
      // Create the tasks table
      await pool.query(`
        CREATE TABLE tasks (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          title TEXT NOT NULL CHECK (length(title) >= 1 AND length(title) <= 255),
          description TEXT,
          completed BOOLEAN NOT NULL DEFAULT FALSE,
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
      `);

      // Create the trigger to update updated_at on modification
      await pool.query(`
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
           NEW.updated_at = CURRENT_TIMESTAMP;
           RETURN NEW;
        END;
        $$ language 'plpgsql';

        CREATE TRIGGER update_tasks_updated_at
            BEFORE UPDATE ON tasks
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
      `);

      console.log('Database schema created successfully');
    } else {
      console.log('Database schema already exists');
    }
  } catch (error) {
    console.error('Error ensuring database schema:', error);
    throw error;
  }
};

// Export a function to run database initialization
export const initializeDatabase = async (): Promise<void> => {
  try {
    await ensureSchema();
    console.log('Database initialization completed successfully');
  } catch (error) {
    console.error('Failed to initialize database:', error);
    throw error;
  }
};