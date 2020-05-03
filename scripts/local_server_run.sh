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

rm -r "${AMMS_HOME}/amms/src/servables"
rm $AMMS_HOME/amms/data/models/*.pbz2
mkdir -p "${AMMS_HOME}/amms/src/servables"
rm "${AMMS_HOME}/amms/data/config/servables.json"

cp -r $servable_folder/*.py $AMMS_HOME/amms/src/servables
cp -r $servable_folder/*.pbz2 $AMMS_HOME/amms/data/model_load_dir
cp "${servable_folder}/servables.json" $AMMS_HOME/amms/data/config

cd $AMMS_HOME/amms || exit
python api.py
