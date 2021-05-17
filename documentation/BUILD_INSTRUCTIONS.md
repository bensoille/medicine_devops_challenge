# Build instructions
> These steps are handled by [convenience build script](../make_build.sh) and these instructions are here for detailed documentation only

> **Minikube** : Please issue command `eval $(minikube docker-env)` and use *minikube* docker repo directly
> Then `docker run -d -p 5000:5000 --restart=always --name registry registry:2` to launch a local registry for k8s to pull from

## Build *Patient* / publisher
When in `medicine_pubsub/` directory :
`docker -D build -f patient/Dockerfile -t ben_loftorbital/test_patient_0 .`

## Build *Medicine* / consumer