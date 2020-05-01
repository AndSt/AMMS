FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8
LABEL maintainer='Andreas Stephan'

# TODO: should apt-get update be run and installation of additional resources?

RUN mkdir -p /app/data
COPY requirements.txt /app/

# install requirements before code is loaded in order to
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app
# TODO: how to load config file.

EXPOSE 5000
CMD ["python", "api.py"]