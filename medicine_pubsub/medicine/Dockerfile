FROM python:3.11.8-alpine

# set the working directory in the container
WORKDIR /medicine

# copy the dependencies file to the working directory
COPY  medicine/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY medicine/src/medicine.py .
ENV PYTHONUNBUFFERED=1

# # Copy Kafka creds and certs
# ARG KAFKA_CA=certs/ca.pem
# ARG KAFKA_KEY=certs/service.key
# ARG KAFKA_CERT=certs/service.cert

# COPY $KAFKA_CA ./medicine_pubsub/certs/
# COPY $KAFKA_KEY ./medicine_pubsub/certs/
# COPY $KAFKA_CERT ./medicine_pubsub/certs/

# command to run on container start
CMD [ "python", "medicine.py" ]