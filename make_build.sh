#!/bin/bash
#  ____        _ _     _ 
# | __ ) _   _(_) | __| |
# |  _ \| | | | | |/ _` |
# | |_) | |_| | | | (_| |
# |____/ \__,_|_|_|\__,_|

# Minikube special case : use minikube local docker registry
# echo "----- Setting up Minikube local Docker registry -----"
# eval $(minikube docker-env)
# docker run -d -p 32000:32000 --restart=always --name registry registry:2
# __________________________________________________________

cd medicine_pubsub/

echo "----- Building _Patient_ docker image -----"
docker -D build -f patient/Dockerfile -t localhost:32000/ben_loftorbital/test_patient_0 .
docker push localhost:32000/ben_loftorbital/test_patient_0

echo "----- Building _Medicine_ docker image -----"
docker -D build -f medicine/Dockerfile -t localhost:32000/ben_loftorbital/test_medicine_0 .
docker push localhost:32000/ben_loftorbital/test_medicine_0

cd -