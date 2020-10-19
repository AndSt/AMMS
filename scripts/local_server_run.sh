#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Supply name of servable. Folder name and servable must have the same name in order for this script to work."
fi

servable_folder="${AMMS_HOME}/examples/local_servables/${1}"
echo "${servable_folder}"

if [ ! -d "${servable_folder}" ]; then
  echo "Servable does not exist. The folder ${servable_folder} has to exist, if you want to test servable ${1}."
  exit
fi

pip install -r "${servable_folder}/requirements.txt"

# clean and copy new files
$AMMS_HOME/scripts/clean_amms_dir.sh

cp -r $servable_folder/*.py $AMMS_HOME/amms/src/custom_servables
cp -r $servable_folder/*.pbz2 $AMMS_HOME/amms/data/model_load_dir
cp "${servable_folder}/servables.json" $AMMS_HOME/amms/data/config

ROOT_DIR=$AMMS_HOME/amms
cd $AMMS_HOME/amms || exit
PYTHONPATH=$ROOT_DIR python api.py
