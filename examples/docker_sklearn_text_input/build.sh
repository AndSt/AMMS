#!/usr/bin/env bash

echo "Build base docker image"
docker build -t amms_base $AMMS_HOME/amms

echo "Stop previously running versions..."
docker stop sklearn_text_input_example
docker rm sklearn_text_input_example

echo "Build image..."
docker build -t sklearn_text_input_example .

echo "Run image on port 5000..."
docker run -d \
  --name sklearn_text_input_example \
  -p 5000:8090 \
  --volume "$(pwd)"/retrained_model/shared_volume:/shared_volume \
    sklearn_text_input_example:latest