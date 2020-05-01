#!/usr/bin/env bash

cd $AMMS_HOME/amms || echo "AMMS_HOME environment variable is not set. Source the .env file or set it manually."
pytest