#!/usr/bin/env bash

docker run -it -p 5001:5001 \
    -e MY_POD_IP='172.17.0.254' \
    -e LOG_LEVEL='INFO' \
    -e BROADCAST_PROB='0.5' \
    -e FANOUT='2' \
    -e TTL='3' \
    -e LOG_FORMATTER='VERBOSE' \
    -e NUMBER_OF_THREADS='3' \
    -e NUMBER_OF_WORKERS='1' \
    -e TEST_IP='http://192.168.99.100:30616' \
    -m 80M \
    epto:latest