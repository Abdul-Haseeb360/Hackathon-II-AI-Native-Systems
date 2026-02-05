# Quickstart Guide: Cloud Native Todo Chatbot Kubernetes Deployment

## Prerequisites

1. **Docker Desktop with Kubernetes enabled** (preferred) OR **Minikube installed and running**
2. **Helm 3.x** installed
3. **kubectl** installed and configured
4. **Access to AI tools**: Gordon, kubectl-ai, kagent
5. **Neon PostgreSQL account** with connection details
6. **Cohere API key** for natural language processing

## Setup Steps

### 1. Prepare Environment
```bash
# Verify Kubernetes cluster is running
kubectl cluster-info

# Verify Helm is available
helm version

# Clone the Phase-3 codebase (if not already present)
# Ensure you're on the 2-k8s-deployment branch
```

### 2. Configure External Dependencies
```bash
# Create a namespace for the application
kubectl create namespace todo-app

# Store sensitive information in Kubernetes Secrets
kubectl create secret generic neon-db-config \
  --namespace=todo-app \
  --from-literal=DATABASE_URL="your_neon_db_connection_string"

kubectl create secret generic cohere-config \
  --namespace=todo-app \
  --from-literal=COHERE_API_KEY="your_cohere_api_key"
```

### 3. Containerization
```bash
# Use Gordon AI to generate Dockerfiles
# Gordon command to generate frontend Dockerfile
gordon generate dockerfile --project-type=nextjs --output=./frontend/Dockerfile

# Gordon command to generate backend Dockerfile
gordon generate dockerfile --project-type=fastapi --output=./backend/Dockerfile

# Build Docker images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend
```

### 4. Generate Kubernetes Resources
```bash
# Use kubectl-ai to generate Kubernetes deployments and services
kubectl-ai create deployment todo-frontend --image=todo-frontend:latest --port=3000
kubectl-ai create deployment todo-backend --image=todo-backend:latest --port=8000
kubectl-ai create service todo-frontend --type=NodePort --selector=app=todo-frontend
kubectl-ai create service todo-backend --type=ClusterIP --selector=app=todo-backend
```

### 5. Create Helm Chart
```bash
# Initialize Helm chart
helm create todo-chatbot-chart

# Use kagent to optimize the chart structure
# Move generated resources into appropriate template files
# Configure values.yaml with proper parameters
```

### 6. Deploy Application
```bash
# Install the Helm chart
helm install todo-chatbot ./todo-chatbot-chart --namespace=todo-app --create-namespace

# Verify deployment
kubectl get pods --namespace=todo-app
kubectl get services --namespace=todo-app
```

### 7. Access Application
```bash
# Get the NodePort for frontend service
kubectl get service todo-frontend --namespace=todo-app

# Access the application in browser
# URL will be: http://localhost:<NODE_PORT> (for Docker Desktop) or Minikube IP
minikube service todo-frontend --namespace=todo-app --url  # if using Minikube
```

## Validation Commands

### Verify Pods Running
```bash
kubectl get pods --namespace=todo-app
```

### Check Service Connectivity
```bash
kubectl get services --namespace=todo-app
kubectl describe service todo-frontend --namespace=todo-app
```

### Test API Endpoints
```bash
# Port forward to test backend API
kubectl port-forward svc/todo-backend 8000:8000 --namespace=todo-app
# Then test: curl http://localhost:8000/health
```

### Check Logs
```bash
kubectl logs -l app=todo-frontend --namespace=todo-app
kubectl logs -l app=todo-backend --namespace=todo-app
```

## Troubleshooting

### If Pods Fail to Start
```bash
# Check pod status and events
kubectl describe pods --namespace=todo-app
kubectl logs <pod-name> --namespace=todo-app
```

### If Services Are Not Accessible
```bash
# Verify service configuration
kubectl describe service todo-frontend --namespace=todo-app
kubectl get nodes -o wide  # for external IP if needed
```

### If Database Connection Fails
```bash
# Verify secrets are properly configured
kubectl get secrets --namespace=todo-app
kubectl describe secret neon-db-config --namespace=todo-app
```