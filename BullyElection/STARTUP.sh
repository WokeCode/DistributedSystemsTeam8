minikube start

clear
echo "Configuring docker enviornment"
sleep 5

eval $(minikube docker-env)

sleep 5
clear
echo "Building Docker"
sleep 5


docker build -t bully-app:0.0.1 .

sleep 5
clear
echo "Building image"
sleep 5

kubectl run bully-app --image=bully-app:0.0.1 --image-pull-policy=Never

sleep 5
clear
echo "Ensuring image creation"
sleep 5

kubectl get pods

sleep 5
clear
echo "Building deployment"
sleep 5

docker build -t bully-app .

sleep 5
clear
echo "Setting up headless servise"
sleep 5

kubectl apply -f k8s/headless-service.yaml

sleep 5
clear
echo "Applying up deployment"
sleep 5

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

clear
loading_bar 5


kubectl get pods