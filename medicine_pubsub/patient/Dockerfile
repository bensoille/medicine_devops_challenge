FROM python:3.8-alpine

# set the working directory in the container
WORKDIR /patient

# copy the dependencies file to the working directory
COPY  patient/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY patient/src/patient.py .
ENV PYTHONUNBUFFERED=1

# # Copy Kafka creds and certs
# ARG KAFKA_CA=certs/ca.pem
# ARG KAFKA_KEY=certs/service.key
# ARG KAFKA_CERT=certs/service.cert

# COPY $KAFKA_CA ./medicine_pubsub/certs/
# COPY $KAFKA_KEY ./medicine_pubsub/certs/
# COPY $KAFKA_CERT ./medicine_pubsub/certs/

# command to run on container start
CMD [ "python", "patient.py" ]