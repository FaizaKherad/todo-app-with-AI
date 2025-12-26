// Database utility functions

import { ensureSchema } from './db';

// Function to ensure the database schema is ready before performing operations
export const ensureDbReady = async (): Promise<void> => {
  try {
    // This will check if the schema exists and create it if needed
    await ensureSchema();
  } catch (error) {
    console.error('Database not ready:', error);
    throw error;
  }
};