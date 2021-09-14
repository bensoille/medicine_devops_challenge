#!/bin/bash

#  ___        __           
# |_ _|_ __  / _|_ __ __ _ 
#  | || '_ \| |_| '__/ _` |
#  | || | | |  _| | | (_| |
# |___|_| |_|_| |_|  \__,_|

echo "----- Installing Kafka stack with Strimzi -----"
#kubectl apply -f 'https://strimzi.io/install/latest?namespace=default' -n default
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka'
echo "-- Successfully installed following crds"
kubectl get crds | grep kafka

echo "----- Deploying Kafka services -----"
#kubectl apply -f deploy/kafka-strimzi.yaml -n default
kubectl apply -f deploy/kafka-strimzi.yaml
echo '-- Waiting for Kafka deployment (can take several minutes, please be patient)'
#kubectl wait kafka/medicine-pubsub --for=condition=Ready --timeout=1200s -n default
kubectl wait kafka/medicine-pubsub --for=condition=Ready --timeout=1200s -n kafka

#echo "----- Installing KEDA -----"
#kubectl apply -f deploy/keda-2.2.0.yaml

echo "----- Creating Topics in Kafka -----"
echo "-- topic tabs.orders"
kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 18 --replication-factor 1 --topic tabs.orders
echo "-- topic tabs.deliveries"
kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 3 --replication-factor 1 --topic tabs.deliveries
echo "-- topic tabs.dlq"
kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 3 --replication-factor 1 --topic tabs.dlq
