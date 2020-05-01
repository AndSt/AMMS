#!/usr/bin/env bash

echo "Stop previously running versions..."
docker stop model_text_server_test
docker rm model_text_server_test

echo "Build image..."
docker build -t model_text_server ../amms/

echo "Run image on port 5000..."
docker run -d \
  --name model_text_server_test \
  -p 5000:5000 \
  --volume "$(pwd)"/retrained_model/shared_volume:/shared_volume \
    model_text_server:latest
