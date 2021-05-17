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
- Minikube running
- Docker
- `kubectl` installed
- `bash` installed

Optional resources :
- Kafka credentials (only needed for external *Kafka* service, not used in current automatic setup)

## Prepare infra
> A [convenience script](make_infra.sh) is available for *bash*. That shell script performs all setup tasks

See [detailed instructions](documentation/PREPARE_INFRA.md) and learn what this [convenience script](make_infra.sh) sets up for you :
- deploys Kafka service to kubernetes
- deploys KEDA facilities to kubernetes
- creates required topics in Kafka

## Build instructions
> A [convenience build script](make_build.sh) is available for *bash* and **minikube**. That shell script performs all build tasks

See [detailed build instructions](documentation/BUILD_INSTRUCTIONS.md) and learn what this [convenience build script](make_build.sh) does for you :
- starts a local docker registry in *minikube*
- builds *patient* and *medicine* Docker images
- and tags images to local *minikube* Docker registry

## Deploy instructions
> A [convenience deploy script](make_deploy.sh) is available for *bash*. That shell script performs all deploy tasks

See [detailed deploy instructions](documentation/DEPLOY_INSTRUCTIONS.md) and learn what this [convenience deploy script](make_deploy.sh) does for you :
- deploys *patient* as a *deployment* to kubernetes
- deploys *medicine* as a *scaledJob* to kubernetes
  
## See it work
### List Kafka topics
`kubectl exec -it medicine-pubsub-kafka-0 -- bin/kafka-topics.sh --list --bootstrap-server medicine-pubsub-kafka-bootstrap:9092`
Optionally log in to Kafka bin with `kubectl exec -it medicine-pubsub-kafka-0 /bin/bash`
### Logs
### Add more patients

# Yet to be done