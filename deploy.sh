#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Ensure IMAGE_TAG is set, defaulting to "latest" if not provided
IMAGE_TAG=${IMAGE_TAG:-latest}

# Navigate to the working directory
cd "$WORKING_DIRECTORY" || { echo "Directory $WORKING_DIRECTORY not found"; exit 1; }

# Enable Docker Buildx if not already enabled
docker buildx create --use || echo "Buildx already enabled"

# Build the Docker image for the correct architecture
echo "Building Docker image with tag: $IMAGE_TAG for linux/amd64..."
docker buildx build --platform linux/amd64 -t "$REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG" --push .

# Log in to the container registry
echo "Logging in to the container registry..."
echo "$REGISTRY_PASSWORD" | docker login "$REGISTRY_URL" -u "$REGISTRY_USERNAME" --password-stdin

# Push the Docker image to the registry
echo "Pushing Docker image to the registry..."
docker push "$REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG"

# Deploy to Azure App Service with the Docker image
echo "Deploying to Azure App Service..."
az webapp config container set --name "$AZURE_APP_NAME" \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --container-image-name "$REGISTRY_URL/$IMAGE_NAME:$IMAGE_TAG"

echo "Deployment completed with tag: $IMAGE_TAG!"
