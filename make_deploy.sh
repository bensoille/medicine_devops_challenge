#!/bin/bash

echo "----- Deploying patient to kubernetes -----"
kubectl apply -f deploy/patient.yaml -n default

