#!/bin/bash

#  ___        __           
# |_ _|_ __  / _|_ __ __ _ 
#  | || '_ \| |_| '__/ _` |
#  | || | | |  _| | | (_| |
# |___|_| |_|_| |_|  \__,_|


echo "----- Installing Redis cluster with Bitnami -----"
# alias kubectl='sudo microk8s kubectl'
# alias helm='sudo microk8s helm3'
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install redis-cluster-medicine bitnami/redis-cluster

# To get your password run:
#     export REDIS_PASSWORD=$(kubectl get secret --namespace "default" redis-cluster-medicine -o jsonpath="{.data.redis-password}" | base64 --decode)

# You have deployed a Redis Cluster accessible only from within you Kubernetes Cluster.INFO: The Job to create the cluster will be created.To connect to your Redis&trade; cluster:

# 1. Run a Redis pod that you can use as a client:
kubectl run --namespace default redis-cluster-medicine-client --rm --tty -i --restart='Never' \
 --env REDIS_PASSWORD=$REDIS_PASSWORD \
--image docker.io/bitnami/redis-cluster:6.2.5-debian-10-r32 -- bash

# 2. Connect using the Redis&trade; CLI:

# redis-cli -c -h redis-cluster-medicine -a $REDIS_PASSWORD





# NOTE : uncomment if using minikube
#echo "----- Installing KEDA -----"
#kubectl apply -f deploy/keda-2.2.0.yaml

