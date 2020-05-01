# AMMS - Another Multi Model Server

Status: Still in heavy development, thus most things are broken.

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