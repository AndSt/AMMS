# AMMS - Another Multi Model Server

Status: Still in heavy development, thus most things are broken.

### Design decisions

- Be close to the awesome tensorflow serving
- Keep number of dependencies minimal to allow extensions dependent
on ML library or its version, i.e. Sklearn 21.1 vs 22.1.
- Minimal framework serving multiple models: 
  - Only one version policy
  - Consequently only one reloading policy
  - Only Metadata and Prediction endpoint

### Techstack

- FastAPI
- FastAPI utils
- Docker

### Next Steps

Some ideas, mainly for myself.

#### Ideas are there
- Testing
    - Test for built dockers  
    - Increase test coverage 
    - Test script to help write new Models(ModelWrapper) 
- More logging
- Keras example; maybe more complicated, where input transformation/validation 
is performed.
- Get compose retrain example running
- small README for local_servables and docker_sklearn_text_input. 
Make sure to clarify why servables.json is loaded in Docker file while it's 
loaded in 'config:' in compose example

#### Cool stuff I'm unsure about
- Meta programming: Try to add dynamically created routs in order to 
get a better Swagger/Redoc defintion
- Change servables.json during runtime (docker exec/sshor similar) such that
it's only working in case servables.json is not broken; alternative would be 
bringing in new containers with new servables.json. Easy on K8s but what's 
going on in Swarm?


### What's included

#### app/
Here is the server, the rest is more or less just a playground so far

#### config/
Examplatory configs

#### retrain/

A simple retraining script using metaflow to test model reloading

#### shared_volume/

Future use cases might allow to load models from S3 buckets or similar.
In here, a shared docker volume will be used.


