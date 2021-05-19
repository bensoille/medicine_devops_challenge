# Prepare infra
> These steps are handled by [convenience script](../make_infra.sh) and these instructions are here for detailed documentation only

## Deploy *Kafka* stack to *Kubernetes* cluster
Kafka service is embedded in this application. It must be deployed to our cluster :
```shell
kubectl apply -f deploy/kafka-strimzi.yaml -n default
```
And then wait for deployment to be ready ; may take several minutes

> See topics in Kafka service with `kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --list --bootstrap-server medicine-pubsub-kafka-bootstrap:9092`

## Create Kafka topics
Topics must be created in first hand. Special attention should be paid to partitions counts. Indeed, a too low value would prevent production of tabs to be  in line with patients tabs orders.
```shell
kubectl exec -it medicine-pubsub-kafka-0 \
-- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 18 --replication-factor 1 --topic tabs.orders

kubectl exec -it medicine-pubsub-kafka-0 \
-- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 3 --replication-factor 1 --topic tabs.deliveries

kubectl exec -it medicine-pubsub-kafka-0 \
-- bin/kafka-topics.sh --create --bootstrap-server medicine-pubsub-kafka-bootstrap:9092 --partitions 3 --replication-factor 1 --topic tabs.dlq
```

## Deploy *KEDA* stack to *Kubernetes* cluster
[KEDA autoscaler](https://keda.sh/) is used in this application and should be deployed to cluster :
```shell
kubectl apply -f deploy/keda-2.2.0.yaml
```
