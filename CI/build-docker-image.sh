#!/bin/bash

# Variables
source ./variables.sh

# Build the docker image
 docker build --platform=linux/arm64 -t $imageName:$tag -f Dockerfile --build-arg FILENAME=$docAppFile --build-arg PORT=$port .