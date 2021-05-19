# Deploy instructions
> These steps are handled by [convenience deploy script](../make_deploy.sh) and these instructions are here for detailed documentation only

## Push docker images to *Kubernetes* cluster repository
If using *minikube*, should be done already while building Docker images in Build instructions paragraph. Docker images are available for k8s to pull.

## Deploy *Patient* and *Medicine*

### *Patient* as a *Deployment*
This is a **Deployment**, which will be looked after by k8s :
```shell
kubectl apply -f deploy/patient.yaml -n default
```

### *Medicine* as a *ScaledJob*
This is a *KEDA* **ScaledJob**, will be launched depending on `tabs.orders` message queue :
```shell
kubectl apply -f deploy/medicine.yaml -n default
```
