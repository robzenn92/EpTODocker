#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
export PYTHONPATH="../"
export BROADCAST_PROB='0.5'
export FANOUT='2'
export TTL='3'
export LOG_LEVEL='INFO'
export LOG_LEVEL='DEBUG'
export LOG_FORMATTER='STANDARD'
export KUBECONFIG="../kubernetesClient/config"
#export TEST_IP='http://192.168.99.100:30616'
exec gunicorn --bind 0.0.0.0:5001 --workers 1 --threads 3 epto_project.wsgi:application