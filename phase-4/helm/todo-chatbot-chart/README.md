# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application to Kubernetes, consisting of a Next.js frontend and a FastAPI backend.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `todo-chatbot`:

```bash
helm install todo-chatbot ./todo-chatbot-chart --namespace todo-app --create-namespace
```

## Uninstalling the Chart

To uninstall the `todo-chatbot` deployment:

```bash
helm uninstall todo-chatbot --namespace todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-chatbot chart and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend pods | `1` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `backend.replicaCount` | Number of backend pods | `1` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |

## Secrets Configuration

Before installing the chart, you need to create the following secrets:

1. Neon PostgreSQL connection:
```bash
kubectl create secret generic neon-db-config \
  --namespace todo-app \
  --from-literal=DATABASE_URL="your_neon_connection_string"
```

2. Cohere API key:
```bash
kubectl create secret generic cohere-config \
  --namespace todo-app \
  --from-literal=COHERE_API_KEY="your_cohere_api_key"
```