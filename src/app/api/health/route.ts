import { NextRequest } from 'next/server';
import { pool } from '@/lib/db';

// Handler for GET requests to check database connectivity
export async function GET(request: NextRequest) {
  try {
    // Test the database connection
    await pool.query('SELECT 1');

    return Response.json({
      status: 'success',
      message: 'Database connection is healthy'
    });
  } catch (error) {
    console.error('Database health check failed:', error);
    return Response.json(
      {
        status: 'error',
        message: 'Database connection failed'
      },
      { status: 500 }
    );
  }
}