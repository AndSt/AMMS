FROM python:3.7-slim-buster
LABEL maintainer='Andreas Stephan'

# from https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.2/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=cdfde14f50a171cbfc35a3a10429e2ab0709afe0

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]

# install dependencies
RUN apt-get update&& apt-get install -y curl dumb-init python3-dev build-essential \
# install supercronic
# (from https://github.com/aptible/supercronic/releases)
 && curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic \
# clean up dependencies
 && apt-get purge -y curl \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /retrain/data
COPY src/requirements.txt /retrain/
RUN pip3 install -r /retrain/requirements.txt
# copy train.py as last, as we have changes here
COPY src/train.py /retrain/

ADD src/crontab.sample /etc/crontab



CMD [ "/usr/local/bin/supercronic", "/etc/crontab" ]