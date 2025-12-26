# Quickstart Guide: Local Cloud-Native Deployment (Minikube)

## Overview

This guide provides instructions for deploying and running the Todo application with conversational AI in a local Kubernetes environment using Minikube.

## Prerequisites

- Docker Desktop or Docker Engine
- Minikube (latest version)
- kubectl
- Python 3.11+ (for local development/testing)

## Setup Instructions

### 1. Start Minikube

```bash
minikube start
```

### 2. Build the Docker Image

From the project root directory:

```bash
# Set Minikube Docker environment
eval $(minikube docker-env)

# Build the image (tagged for local Minikube registry)
docker build -t todo-engine:v1.0.0 .
```

### 3. Deploy to Minikube

Apply all Kubernetes manifests:

```bash
kubectl apply -f k8s/
```

This will create:
- Namespace: `todo-phase-iv`
- PVC for persistent storage
- MCP server deployment and service
- Todo app deployment and service

### 4. Verify Deployment

Check that all resources are running:

```bash
kubectl get pods -n todo-phase-iv
kubectl get services -n todo-phase-iv
kubectl get pvc -n todo-phase-iv
```

### 5. Access the Application

The todo application is exposed as a NodePort service. To access it:

```bash
# Get the service URL
minikube service todo-app-service -n todo-phase-iv --url
```

Alternatively, you can use kubectl exec to access the pod directly:

```bash
kubectl exec -it -n todo-phase-iv deploy/todo-app -- python main.py
```

## Using the Application

Once connected to the application, you can use the same commands as in previous phases:

### CLI Commands

```bash
# Add a task
python main.py add --title "My task" --description "Task description"

# List tasks
python main.py list

# Update a task
python main.py update --id <task-id> --title "New title"

# Delete a task
python main.py delete --id <task-id>

# Mark task as complete
python main.py complete --id <task-id>

# Use AI interface
python main.py ai --prompt "Add a task to buy groceries"
```

### AI Conversational Interface

Start the AI interface for natural language interaction:

```bash
python main.py ai
```

Then use natural language commands like:
- "Add a task to buy groceries"
- "Show my tasks"
- "Mark the grocery task as complete"
- "Update the grocery task description"

## Troubleshooting

### Common Issues

1. **ImagePullBackOff Error**
   - Ensure you've built the image in the Minikube Docker environment
   - Run: `eval $(minikube docker-env)` then rebuild the image

2. **PVC Pending**
   - Minikube should have a default storage provisioner
   - Check: `kubectl get storageclass`

3. **Service Unreachable**
   - Use `minikube service` command to get the correct URL
   - Verify the pod is in Running state

### Checking Logs

```bash
# View application logs
kubectl logs -n todo-phase-iv deploy/todo-app

# View application logs in real-time
kubectl logs -n todo-phase-iv -f deploy/todo-app

# View specific pod logs
kubectl logs -n todo-phase-iv <pod-name>
```

## Cleaning Up

To remove the deployment:

```bash
kubectl delete -f k8s/
```

To stop Minikube:

```bash
minikube stop
```

## Architecture Overview

The deployed system consists of:

- **todo-app**: Contains the core Todo Engine and AI assistant
- **mcp-server**: Internal service for MCP tool exposure (internal cluster use only)
- **PersistentVolumeClaim**: Ensures task data survives pod restarts
- **Services**: Expose applications within the cluster and externally

The system maintains all functionality from Phases I-III while adding cloud-native deployment capabilities.