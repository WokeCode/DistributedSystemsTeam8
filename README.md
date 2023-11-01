# DistributedSystemsTeam8
Repository for group projects, for Distributed Systems 2023, to setup reboot and startup commands enter 
'chmod +x SHUTDOWN.sh', 'chmod +x REBOOT.sh' and 'chmod +x STARTUP.sh' in terminal at repo directory. On startup enter './STARTUP.sh' in terminal window, and on reboot './REBOOT.sh'

## SETUP (linux)

minikube start


eval $(minikube docker-env)


docker build -t bully-app:0.0.1 .


kubectl run bully-app --image=bully-app:0.0.1 --image-pull-policy=Never


kubectl get pods


docker build -t bully-app .


kubectl apply -f k8s/headless-service.yaml


kubectl apply -f k8s/deployment.yaml


kubectl get pods



## FOR RESTART
kubectl delete pods --all


kubectl delete deployments --all


minikube stop


minikube delete



## TO SEE ACTIVITIES
kubectl logs pod-name


## SETUP (Windows)

minikube start


minikube docker-env | Invoke-Expression


docker build -t bully-app:0.0.1 .


kubectl run bully-app --image=bully-app:0.0.1 --image-pull-policy=Never


kubectl get pods


docker build -t bully-app .


kubectl apply -f k8s/headless-service.yaml


kubectl apply -f k8s/deployment.yaml

