#!/usr/bin/env bash

docker build -t model_text_server ../amms/ \
  --build-arg MODEL_NAME="general_fields_payment_mode" \
	--build-arg ASPIRED_VERSION="1.0.1" \
	--build-arg LOAD_TYPE="shared" \
	--build-arg LOAD_PATH="/shared_volume"
