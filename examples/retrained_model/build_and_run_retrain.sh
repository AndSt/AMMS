#!/usr/bin/env bash

docker build -t retrain_model .

docker stop retrain_model
docker rm retrain_model

docker run -d \
  --name retrain_model \
  -p 7123:7123 \
  --env-file .env \
  --volume "$(pwd)"/shared_volume:/shared_volume \
    retrain_model:latest

