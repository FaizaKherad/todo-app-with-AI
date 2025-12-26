import { NextRequest } from 'next/server';
import { initializeDatabase } from '@/lib/db';

// Initialize the database when this endpoint is called
export async function GET(request: NextRequest) {
  try {
    await initializeDatabase();
    return Response.json({ 
      success: true,
      message: 'Database initialized successfully' 
    });
  } catch (error) {
    console.error('Failed to initialize database:', error);
    return Response.json(
      { 
        success: false,
        message: 'Failed to initialize database',
        error: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}