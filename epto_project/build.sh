#!/usr/bin/env bash

eval $(minikube docker-env)
docker build -f epto_project/Dockerfile -t epto:latest .