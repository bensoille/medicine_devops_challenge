#!/bin/bash

echo "----- Installing Kafka stack with Strimzi -----"
kubectl apply -f 'https://strimzi.io/install/latest?namespace=default' -n default
echo "-- Successfully installed following crds"
kubectl get crds | grep kafka

echo "----- Deploying Kafka services -----"
kubectl apply -f deploy/kafka-strimzi.yaml -n default
echo "-- Waiting for Kafka deployment (can take several minutes, please be patient)"
kubectl wait kafka/medicine-pubsub --for=condition=Ready --timeout=1200s -n default

echo "----- Installing KEDA -----"
kubectl apply -f deploy/keda-2.2.0.yaml

echo "----- Creating Topics in Kafka -----"
echo "-- topic tabs.orders"
kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 1 --replication-factor 1 --topic tabs.orders
echo "-- topic tabs.deliveries"
kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 1 --replication-factor 1 --topic tabs.deliveries
echo "-- topic tabs.dlq"
kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 1 --replication-factor 1 --topic tabs.dlq

echo "----- Building _Patient_ docker image -----"


echo "----- Building _Medicine_ docker image -----"