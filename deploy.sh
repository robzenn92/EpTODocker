#!/usr/bin/env bash

sh build.sh
if [ $? -eq 0 ]; then
    kubectl delete deployment epto-deployment
    kubectl create -f deployment.yml
    kubectl get pod -o wide
fi
