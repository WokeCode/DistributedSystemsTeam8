# DistributedSystemsTeam8
Repository for group projects, for Distributed Systems 2023

## SETUP
Copy paste follwing lines to terminal (Unix)

minikube start


eval $(minikube docker-env)


docker build -t foo:0.0.1 .


kubectl run hello-foo --image=foo:0.0.1 --image-pull-policy=Never


kubectl get pods


docker build -t bully-app .


kubectl apply -f k8s/headless-service.yaml


kubectl apply -f k8s/deployment.yaml
