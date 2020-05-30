#!/usr/bin/env bash

echo "Stop previously running versions..."
docker stop model_text_server_test
docker rm model_text_server_test

echo "Build image..."
docker build -t model_text_server  "${AMMS_HOME}"/examples/local_servables/sklearn_text_input/

echo "Run image on port 5000..."
docker run -d \
  --name model_text_server_test \
  -p 5000:8090 \
  --volume "${AMMS_HOME}"/examples/docker_compose_sklearn_retraining/shared_volume:/shared_volume \
    model_text_server:latest
