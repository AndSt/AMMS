FROM tiangolo/uvicorn-gunicorn:python3.8-slim
LABEL maintainer='Andreas Stephan'

RUN mkdir -p /app/data
COPY requirements.txt /app/

# install requirements before code is loaded in order to
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app
