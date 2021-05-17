# Deploy instructions
> These steps are handled by [convenience deploy script](../make_deploy.sh) and these instructions are here for detailed documentation only

## Push docker images to *Kubernetes* cluster repository
If using *minikube*, should be done already while building Docker images in Build instructions paragraph.

## Deploy *Patient* and *Medicine*

### *Patient* as a *Deployment*
`kubectl apply -f deploy/patient.yaml -n default`

### *Medicine* as a *ScaledJob*