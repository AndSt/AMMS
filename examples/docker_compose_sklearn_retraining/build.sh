#!/usr/bin/env bash

cd $AMMS_HOME/examples/docker_compose_sklearn_retraining/amms
docker build -t model_server .

cd $AMMS_HOME/examples/docker_compose_sklearn_retraining/retrain
docker build -t retrain .

cd $AMMS_HOME/examples/docker_compose_sklearn_retraining/
docker-compose up