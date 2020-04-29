FROM python:3.7-slim-buster
LABEL maintainer='Andreas Stephan'

ARG TRAIN_DIR

RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /retrain
RUN mkdir -p /retrain/data
COPY requirements.txt /retrain/

WORKDIR /app
RUN pip3 install -r requirements.txt

# install requirements before code is loaded
COPY src /retrain/
RUN ls /retrain

EXPOSE 6000
CMD ["sh", "train.sh"]