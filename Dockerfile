# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make sure the application runs on the expected port (for potential web interface)
EXPOSE 8000

# Set up the command to run the application
CMD ["python", "main.py"]