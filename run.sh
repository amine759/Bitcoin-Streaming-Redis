#!/bin/bash

NETWORK_NAME="mynetwork"

# Check if the network exists
if ! docker network inspect "$NETWORK_NAME" &> /dev/null; then
    echo "Network $NETWORK_NAME not found. Creating the network..."
    docker network create "$NETWORK_NAME"
else
    echo "Network $NETWORK_NAME already exists."
fi

# Check if the Redis image exists locally
if [ ! "$(docker images -q redis:latest)" ]; then
    echo "Redis image not found locally. Pulling Redis image..."
    docker pull redis:latest
fi

# Check if the Redis container is already running
if [ ! "$(docker ps -q -f name=some-redis)" ]; then
    echo "Redis container not running. Starting Redis container..."
    docker run -d --name some-redis --network "$NETWORK_NAME" redis:latest
else
    echo "Redis container already running."
fi

sleep 1
if [ "$(docker images -aq btc-stream)" ]; then
    echo "btc-stream image already exists. rebuilding it..."
    docker rmi -f btc-stream
    sleep 1
    docker build -t btc-stream .
else
    docker build -t btc-stream .
fi

sleep 1

if [ "$(docker ps -aq -f name=btc-app)" ]; then
    echo "btc-app container already up and running. restarting it..."
    docker restart btc-app
else
    echo "running btc-app container..."
    docker run -d -p 4500:8080 --name btc-app --network "$NETWORK_NAME" btc-stream
fi

sleep 1
echo "running btc-app container..."
python3 -m webbrowser http://localhost:4500/