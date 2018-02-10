#!/usr/bin/env bash

docker run -it \
    -e APP='epto' \
    -e DEPLOYMENT_NAME='epto-deployment' \
    -e LOG_LEVEL='DEBUG' \
    -e LOG_FORMATTER='STANDARD' \
    kubeclient:latest