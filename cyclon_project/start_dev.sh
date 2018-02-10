#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
export PYTHONPATH="../"
export APP='epto'
export DEPLOYMENT_NAME='epto-deployment'
export MY_POD_IP='172.17.0.254'
export VIEW_LIMIT='4'
export SHUFFLE_LENGTH='3'
export LOG_LEVEL='DEBUG'
export LOG_FORMATTER='STANDARD'
#export TEST_IP='http://192.168.99.100:30616'
exec gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 3 cyclon_project.wsgi:application