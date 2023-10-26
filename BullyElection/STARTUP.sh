minikube start


eval $(minikube docker-env)


docker build -t bully-app:0.0.1 .


kubectl run bully-app --image=bully-app:0.0.1 --image-pull-policy=Never


kubectl get pods


docker build -t bully-app .


kubectl apply -f k8s/headless-service.yaml


kubectl apply -f k8s/deployment.yaml


#!/bin/bash

loading_bar() {
    local duration=$1
    local bar_length=20

    for ((i = 0; i < $bar_length; i++)); do
        echo -ne ""
    done
    echo -n " ["

    for ((i = 0; i < $bar_length; i++)); do
        echo -n ">"
        sleep 0.$((duration * 100 / bar_length)) # Adjust sleep time for the desired duration
    done

    echo "] Done"
}

loading_bar 5


kubectl get pods