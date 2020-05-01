#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Supply name of servable. Folder name and servable must have the same name in order for this script to work."
fi

servable_folder="${AMMS_HOME}/servables/${1}"
echo $servable_folder

if [ ! -d $servable_folder ]; then
  echo "Servable does not exist. The folder ${servable_folder} has to exist, if you want to test servable ${1}."
  exit
fi

pip install -r $servable_folder/requirements.txt

rm -r $AMMS_HOME/amms/src/servables
mkdir -p $AMMS_HOME/amms/src/servables

cp "${servable_folder}/${1}.py" $AMMS_HOME/amms/src/servables

#uvicorn api:app --reload --port 8090 --host 0.0.0.0
cd $AMMS_HOME/amms
python api.py
