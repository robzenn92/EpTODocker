#!/usr/bin/env bash

eval $(minikube docker-env)
docker build -f cyclon_project/Dockerfile -t cyclon:latest .