#!/usr/bin/env bash

echo "Running tests."
sh run_tests.sh
if [ $? -eq 0 ]; then
    eval $(minikube docker-env)
    kubectl delete deployment epto-deployment
    sh ./cyclon/build.sh
    sh ./epto/build.sh
    kubectl create -f deployment.yml
    kubectl get pod -o wide
fi

