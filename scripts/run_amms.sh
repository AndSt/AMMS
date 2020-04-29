#!/usr/bin/env bash

if [ $DEVEL = true ]; then
  docker stop model_text_server_test
  docker rm model_text_server_test
  rm app/data/config
fi

docker run -d \
  --name model_text_server_test \
  -p 5000:5000 \
  --volume "$(pwd)"/config/config.json:/app/data/config.json \
  --volume "$(pwd)"/shared_volume:/shared_volume \
    model_text_server:latest
