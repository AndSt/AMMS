FROM amms_base
LABEL maintainer='Andreas Stephan'

WORKDIR /app
COPY requirements.txt /app/

# install requirements before code is models in order to
RUN pip install --no-cache-dir -r requirements.txt
COPY servables.json /app/data/config/

EXPOSE 5000
CMD ["python", "api.py"]