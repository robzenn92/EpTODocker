#!/usr/bin/env bash

docker network create mynet

docker run -d -p 5000:5000 \
    --network mynet \
    -e APP='epto' \
    -e DEPLOYMENT_NAME='epto-deployment' \
    -e MY_POD_IP='172.17.0.254' \
    -e VIEW_LIMIT='4' \
    -e SHUFFLE_LENGTH='3' \
    -e LOG_LEVEL='INFO' \
    -e LOG_FORMATTER='VERBOSE' \
    -e KUBECONFIG="../kubernetesClient/config" \
    -e NUMBER_OF_THREADS='3' \
    -e NUMBER_OF_WORKERS='1' \
    -e TEST_IP='http://192.168.99.100:30616' \
    -m 80M \
    cyclon:latest

docker run -it -p 5001:5001 \
    --network mynet \
    -e MY_POD_IP='172.17.0.254' \
    -e BROADCAST_PROB='0.5' \
    -e FANOUT='2' \
    -e TTL='3' \
    -e LOG_LEVEL='DEBUG' \
    -e LOG_FORMATTER='STANDARD' \
    -e NUMBER_OF_THREADS='3' \
    -e NUMBER_OF_WORKERS='1' \
    -e TEST_IP='http://192.168.99.100:30616' \
    -m 80M \
    epto:latest