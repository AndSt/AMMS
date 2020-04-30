FROM python:3.7-slim-buster
LABEL maintainer='Andreas Stephan'

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /app/data
COPY requirements.txt /app/

# install requirements before code is loaded in order to
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
# load config file.

EXPOSE 5000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "api:app"]