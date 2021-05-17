#!/bin/bash

# Minikube special case : use minikube local docker registry
eval $(minikube docker-env)
docker run -d -p 5000:5000 --restart=always --name registry registry:2

cd medicine_pubsub/

docker -D build -f patient/Dockerfile -t localhost:5000/ben_loftorbital/test_patient_0 .

cd -