FROM python:3.7-slim-buster
LABEL maintainer='Andreas Stephan'

ARG MODEL_NAME
ARG ASPIRED_VERSION
ARG LOAD_TYPE
ARG LOAD_URL

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /app
COPY requirements.txt /app/

# install requirements before code is loaded in order to
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
# load config file.
# TODO: Interchange with loaded volume; ENTRYPOINT or docker-compose configs; or .env file; look how tf-serving is doing it.
RUN echo "{\"model_name\": \"$MODEL_NAME\", \"aspired_version\": \"$ASPIRED_VERSION\", \"load_type\": \"$LOAD_TYPE\", \"load_url\": \"$LOAD_URL\"}" > /app/data/config.json

EXPOSE 5000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "api:app"]