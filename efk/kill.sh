#!/bin/bash

eval $(minikube docker-env)

kubectl delete -f kubernetes_config/es-controller.yaml
kubectl delete -f kubernetes_config/es-service.yaml
kubectl delete -f kubernetes_config/kibana-controller.yaml
kubectl delete -f kubernetes_config/kibana-service.yaml
kubectl --namespace kube-system delete configmap fluentd-config
kubectl delete -f kubernetes_config/fluentd-daemonset.yaml