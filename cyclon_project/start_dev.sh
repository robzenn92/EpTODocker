#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
export PYTHONPATH="../"
export APP='epto'
export DEPLOYMENT_NAME='epto-deployment'
export MY_POD_IP='172.17.0.254'
export VIEW_LIMIT='4'
export SHUFFLE_LENGTH='3'
export LOG_LEVEL='INFO'
export LOG_DATE_FORMAT='%Y-%m-%d,%H:%M:%S'
export LOG_FORMAT='[%(asctime)s.%(msecs)03d - %(levelname)s] %(filename)s:%(lineno)d | %(funcName)s - %(message)s'
export KUBECONFIG="../kubernetesClient/config"
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 3 cyclon_project.wsgi:application