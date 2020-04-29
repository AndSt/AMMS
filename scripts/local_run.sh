#!/usr/bin/env bash

cp config/config.json app/data/
cd app
uvicorn api:app --reload --port 8090 --host 0.0.0.0
