#!/usr/bin/env bash

export PYTHONPATH="../"
export APP='epto'
export DEPLOYMENT_NAME='epto-deployment'
export LOG_LEVEL='DEBUG'
export LOG_FORMATTER='STANDARD'
export KUBECONTEXT='epto.cluster.k8s.local'
python kubernetesClient.py