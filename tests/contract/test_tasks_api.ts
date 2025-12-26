// API Contract tests for the Todo Application
// These tests verify that the API endpoints follow the specified contract

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

// Test the GET /api/tasks endpoint
async function testGetTasks() {
  try {
    const response = await fetch(`${BASE_URL}/api/tasks`);
    const result = await response.json();
    
    if (response.status === 200) {
      console.log('✓ GET /api/tasks: Success response format is correct');
      if (Array.isArray(result.data)) {
        console.log('✓ GET /api/tasks: Returns array of tasks');
      } else {
        console.log('✗ GET /api/tasks: Does not return array of tasks');
      }
    } else {
      console.log('✗ GET /api/tasks: Failed with status', response.status);
    }
  } catch (error) {
    console.log('✗ GET /api/tasks: Error occurred', error);
  }
}

// Test the POST /api/tasks endpoint
async function testCreateTask() {
  try {
    const taskData = {
      title: "Test task for API contract",
      description: "This is a test task to verify the API contract"
    };
    
    const response = await fetch(`${BASE_URL}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    
    const result = await response.json();
    
    if (response.status === 201) {
      console.log('✓ POST /api/tasks: Success response format is correct');
      if (result.data && result.data.id) {
        console.log('✓ POST /api/tasks: Returns created task with ID');
        return result.data.id; // Return the ID for future tests
      } else {
        console.log('✗ POST /api/tasks: Does not return task with ID');
      }
    } else if (response.status === 400) {
      console.log('✗ POST /api/tasks: Validation error occurred', result);
    } else {
      console.log('✗ POST /api/tasks: Failed with status', response.status);
    }
  } catch (error) {
    console.log('✗ POST /api/tasks: Error occurred', error);
  }
  
  return null;
}

// Test the PUT /api/tasks/{id} endpoint
async function testUpdateTask(taskId: string) {
  if (!taskId) {
    console.log('⚠️  PUT /api/tasks/{id}: Skipping test - no task ID available');
    return;
  }
  
  try {
    const taskData = {
      title: "Updated test task",
      description: "This is an updated test task"
    };
    
    const response = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    
    const result = await response.json();
    
    if (response.status === 200) {
      console.log('✓ PUT /api/tasks/{id}: Success response format is correct');
      if (result.data && result.data.id === taskId) {
        console.log('✓ PUT /api/tasks/{id}: Returns updated task with correct ID');
      } else {
        console.log('✗ PUT /api/tasks/{id}: Does not return task with correct ID');
      }
    } else if (response.status === 400) {
      console.log('✗ PUT /api/tasks/{id}: Validation error occurred', result);
    } else if (response.status === 404) {
      console.log('✗ PUT /api/tasks/{id}: Task not found', result);
    } else {
      console.log('✗ PUT /api/tasks/{id}: Failed with status', response.status);
    }
  } catch (error) {
    console.log('✗ PUT /api/tasks/{id}: Error occurred', error);
  }
}

// Test the DELETE /api/tasks/{id} endpoint
async function testDeleteTask(taskId: string) {
  if (!taskId) {
    console.log('⚠️  DELETE /api/tasks/{id}: Skipping test - no task ID available');
    return;
  }
  
  try {
    const response = await fetch(`${BASE_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
    
    const result = await response.json();
    
    if (response.status === 200) {
      console.log('✓ DELETE /api/tasks/{id}: Success response format is correct');
      if (result.data && result.data.success === true) {
        console.log('✓ DELETE /api/tasks/{id}: Returns success confirmation');
      } else {
        console.log('✗ DELETE /api/tasks/{id}: Does not return success confirmation');
      }
    } else if (response.status === 404) {
      console.log('✗ DELETE /api/tasks/{id}: Task not found', result);
    } else {
      console.log('✗ DELETE /api/tasks/{id}: Failed with status', response.status);
    }
  } catch (error) {
    console.log('✗ DELETE /api/tasks/{id}: Error occurred', error);
  }
}

// Test the PATCH /api/tasks/{id}/complete endpoint
async function testToggleCompletion(taskId: string) {
  if (!taskId) {
    console.log('⚠️  PATCH /api/tasks/{id}/complete: Skipping test - no task ID available');
    return;
  }
  
  try {
    const response = await fetch(`${BASE_URL}/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
    
    const result = await response.json();
    
    if (response.status === 200) {
      console.log('✓ PATCH /api/tasks/{id}/complete: Success response format is correct');
      if (result.data && result.data.id === taskId) {
        console.log('✓ PATCH /api/tasks/{id}/complete: Returns updated task with correct ID');
      } else {
        console.log('✗ PATCH /api/tasks/{id}/complete: Does not return task with correct ID');
      }
    } else if (response.status === 404) {
      console.log('✗ PATCH /api/tasks/{id}/complete: Task not found', result);
    } else {
      console.log('✗ PATCH /api/tasks/{id}/complete: Failed with status', response.status);
    }
  } catch (error) {
    console.log('✗ PATCH /api/tasks/{id}/complete: Error occurred', error);
  }
}

// Run all tests
async function runTests() {
  console.log('Starting API Contract Tests...\n');
  
  await testGetTasks();
  const taskId = await testCreateTask();
  await testUpdateTask(taskId);
  await testToggleCompletion(taskId);
  await testDeleteTask(taskId);
  
  console.log('\nAPI Contract Tests Completed!');
}

// Execute the tests
runTests().catch(console.error);