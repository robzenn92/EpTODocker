#!/usr/bin/env bash

eval $(minikube docker-env)
docker build -f epto/Dockerfile -t epto:latest .