#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Set your variables
GIT_USERNAME="nhatthanh020996"
GIT_REPO_NAME="fastapi-docker-swarm-init"  # Replace with your Git repository URL
IMAGE_NAME="nhatthanh020996/fastapi-swarm-webserver"              # Replace with your Docker image name
SERVICE_NAME="dms-ws_webserver"                                       # Replace with your Docker Swarm service name

# Get the short version of the latest commit hash from the origin/master branch
COMMIT_HASH=$(git rev-parse --short origin/master)
echo "Latest commit hash from master: $COMMIT_HASH"

# Build the Docker image with the tag
git fetch origin master
git checkout origin/master
echo "Building the Docker image..."
docker build -t $IMAGE_NAME:$COMMIT_HASH .
docker build -t $IMAGE_NAME:latest .

# Push the Docker image to Docker Hub
echo "Pushing the Docker image to Docker Hub..."
docker push $IMAGE_NAME:$COMMIT_HASH
docker push $IMAGE_NAME:latest

# Update the Docker Swarm service with the new image
echo "Updating the Docker Swarm service..."
docker service update --with-registry-auth --image $IMAGE_NAME:$COMMIT_HASH --update-order start-first --force $SERVICE_NAME

# Check if the service update was successful
echo "Checking service update status..."
UPDATE_STATUS=$(docker service inspect --format="{{.UpdateStatus.State}}" $SERVICE_NAME)

if [ "$UPDATE_STATUS" == "completed" ]; then
  echo "Service updated successfully!"

  # Find and delete the older versions of the Docker image
  echo "Cleaning up old Docker images..."
  docker images --format "{{.ID}} {{.Repository}}:{{.Tag}}" | grep $IMAGE_NAME | grep -v $COMMIT_HASH | while read -r IMAGE_ID IMAGE_TAG
  do
    echo "Removing old image: $IMAGE_TAG"
    docker image rm -f $IMAGE_ID
  done
else
  echo "Service update failed or is still in progress."
  exit 1
fi

echo "Script completed successfully."