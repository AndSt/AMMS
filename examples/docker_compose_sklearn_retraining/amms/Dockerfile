FROM amms_base
LABEL maintainer='Andreas Stephan'


COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY servables.json /app/data/config/
COPY *.py /app/src/servables/
RUN mkdir /shared_volume
COPY *.pbz2 /shared_volume
# install requirements before code is loaded in order to

EXPOSE 5000
CMD ["python", "api.py"]