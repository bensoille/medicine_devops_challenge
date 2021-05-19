#!/bin/bash

#  ____             _             
# |  _ \  ___ _ __ | | ___  _   _ 
# | | | |/ _ \ '_ \| |/ _ \| | | |
# | |_| |  __/ |_) | | (_) | |_| |
# |____/ \___| .__/|_|\___/ \__, |
#            |_|            |___/ 

echo "----- Deploying medicine maker to kubernetes -----"
kubectl apply -f deploy/medicine.yaml -n default

# Wait 2 seconds and allow coldstart
sleep 2

echo "----- Deploying patient to kubernetes -----"
kubectl apply -f deploy/patient.yaml -n default
