#!/bin/bash

# Minikube special case : use minikube local docker registry
echo "----- Setting up Minikube local Docker registry -----"
eval $(minikube docker-env)
docker run -d -p 5000:5000 --restart=always --name registry registry:2

cd medicine_pubsub/

echo "----- Building _Patient_ docker image -----"
docker -D build -f patient/Dockerfile -t localhost:5000/ben_loftorbital/test_patient_0 .

echo "----- Building _Medicine_ docker image -----"

cd -