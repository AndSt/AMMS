#!/usr/bin/env bash

rm -r "${AMMS_HOME}/amms/src/custom_servables"
mkdir -p "${AMMS_HOME}/amms/src/custom_servables"

rm $AMMS_HOME/amms/data/models/*.pbz2
rm "${AMMS_HOME}/amms/data/config/servables.json"