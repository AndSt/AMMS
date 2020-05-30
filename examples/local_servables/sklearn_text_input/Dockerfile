FROM amms_base
LABEL maintainer='Andreas Stephan'


COPY requirements.txt /app/

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY servables.json /app/data/config/
COPY ../../docker_compose_sklearn_retraining/amms/sklearn_text_input.py /app/src/servables/
RUN ls src
RUN ls src/servables/
# install requirements before code is loaded in order to

EXPOSE 5000
CMD ["python", "api.py"]