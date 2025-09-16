#!/bin/bash

# Container and image names
CONTAINER_NAME=round_bot_dev
IMAGE_NAME=ros2-humble-gazebo-harmonic

# Resolve repo root (this script is inside round_bot/docker/, go two levels up)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Workspace (round_bot_harmonic_ws)
HOST_WS="$REPO_ROOT"

# Create workspace if missing
mkdir -p $HOST_WS

# Run or attach to container
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  if [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
    docker rm $CONTAINER_NAME > /dev/null
  fi
  echo "Starting container $CONTAINER_NAME..."
  docker run -dit \
    --name $CONTAINER_NAME \
    --net=host \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="LIBGL_ALWAYS_INDIRECT=0" \
    --device /dev/dri:/dev/dri \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$HOST_WS:/root/round_bot_harmonic_ws" \
    -w /root/round_bot_harmonic_ws \
    $IMAGE_NAME
fi

echo "Attaching to container $CONTAINER_NAME..."
docker exec -it $CONTAINER_NAME bash
