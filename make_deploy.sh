#!/bin/bash

echo "----- Deploying medicine maker to kubernetes -----"
kubectl apply -f deploy/medicine.yaml -n default

sleep 5

echo "----- Deploying patient to kubernetes -----"
kubectl apply -f deploy/patient.yaml -n default
