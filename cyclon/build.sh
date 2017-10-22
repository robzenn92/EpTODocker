#!/usr/bin/env bash

eval $(minikube docker-env)
docker build -f cyclon/Dockerfile -t cyclon:latest .