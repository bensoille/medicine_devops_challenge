# Medicine PubSub devops challenge

Trying to fight against a epidemy, we must provide with **on demand** medicine tabs production.
Our system must allow additional patients to request tabs without human manual *scale up* action, nor service level degradation.

# Documentation
Please see :
- [Functional specs](WORK_SUMMARY.md) for a quick overview of what the system is doing, and main problems that it overcomes
- [Technical specs](documentation/README.md) for in-depth description 

# Quick start
## Prerequisites
Technical stack :
- Docker
- a running Kubernetes cluster, such as *MiniKube*

Additional resources :
- Kafka credentials

## Prepare infra
> A [convenience build script](make_infra.sh) is available for *ubuntu* OS. That shell script performs all following explained build steps for you
> 
### Deploy *Kafka* stack to *Kubernetes* cluster
> See topics in Kafka service with `kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --list --bootstrap-server medicine-pubsub-kafka-bootstrap:9092`

### Deploy *KEDA* stack to *Kubernetes* cluster

## Build instructions
> A [convenience build script](make_build.sh) is available for *ubuntu* OS. That shell script performs all following explained build steps for you

### Build *Patient* / publisher
### Build *Medicine* / consumer

## Deploy instructions
> A [convenience deploy script](make_deploy.sh) is available for *ubuntu* OS and *MiniKube* k8s flavor. That shell script performs all following explained deploy steps for you

### Push docker images to *Kubernetes* cluster repository
### Deploy *Patient* and *Medicine*
#### *Patient* as a *Deployment*
#### *Medicine* as a *ScaledJob*

## See it work
### Logs
### Add more patients

# Yet to be done