# AMMS - Another Multi Model Server


Status: Still in heavy development, thus most things are broken.

- [Design decisions](#design-decisions)
- [Techstack](#techstack)
- [Next Steps](#next-steps)
  * [Ideas are there](#ideas-are-there)
  * [Cool stuff I'm unsure about](#cool-stuff-i-m-unsure-about)
- [Examples](#examples)
- [What's included](#what-s-included)
  * [app/](#app-)
  * [config/](#config-)
  * [retrain/](#retrain-)
  * [shared_volume/](#shared-volume-)
- [Testing](#testing)
  * [Code testing](#code-testing)
  * [Servable testing](#servable-testing)
  * [API testing](#api-testing)
- [Build you own servables:](#build-you-own-servables-)

### Design decisions

- Be close to the awesome tensorflow serving
    - similar application logic (simpler for sure)
    - same routes
- Keep number of dependencies minimal to allow extensions dependent
on ML library or its version, i.e. Sklearn 21.1 vs 22.1.
- Minimal framework serving multiple models: 
  - Version policy
    - Rather extensive versioning framework 1.x.x (2 subversions possible)
    - Policy's allow reloading during runtime
  - Only Metadata and Prediction endpoints
    - Automatic creation of routes and Swagger/ OpenAPI specification
    - 
 
### Next Steps

Some ideas, mainly for myself.

#### Ideas are there
- Testing
    - Test for built dockers  
    - Increase test coverage 
    - Test API automatically
        - health status, standard ones
        - by asking for available models all router can be tested to achieve
        test coverage; pydantic to Example needs to work fairly well for that
    - Test script to help write new Models(ModelWrapper) 
- More logging
- Keras example; maybe more complicated, where input transformation/validation 
is performed.
- Get compose retrain example running
- small README for local_servables and docker_sklearn_text_input. 
Make sure to clarify why servables.json is loaded in Docker file while it's 
loaded in 'config:' in compose example

#### Cool stuff I'm unsure about

- Change servables.json during runtime (docker exec/sshor similar) such that
it's only working in case servables.json is not broken; alternative would be 
bringing in new containers with new servables.json. Easy on K8s but what's 
going on in Swarm?


### Usage

Make sure to sure .env


### Examples

Look at the [README.md](examples/README.md) in the `examples/` folder. 
Summarized, we give local examples, a Docker, a docker-compose and a 
Docker Swarm example. At least that's intended...

### What's included

- `amms/`: Here is the server, the rest is more or less just a playground so far


### Testing

Testing is really important. If you fork the repository, you can easily test 
your changes. First install the development dependencies with

```console
foo@bar:~$ pip install -r dev_requirements.txt
foo
````

We distinguish between:
- Code testing: Unittests for the `amms/` folder.
- Servable testing: Code provided to test the servables you build.
- API testing: Just provide an endpoint, i.e. URL + Port, and all routes are 
tested automatically based on Pydantic models the API exposes.

#### Code testing

Then you can test the code with the following commands:
```console
foo@bar:~$ pytest  # run all tests
foo@bar:~$ pytest --cov=amms/src amms/tests # check test coverage
foo@bar:~$ --cov=amms/src --cov-report html amms/tests # create HTML files showing code coverage
````

#### Servable testing

#### API testing



### Build you own servables:


### Techstack

- FastAPI
- FastAPI utils
- Docker


