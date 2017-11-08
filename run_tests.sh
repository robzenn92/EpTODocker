#!/usr/bin/env bash

export PYTHONPATH='.'
VIEW_LIMIT=3 SHUFFLE_LENGTH=2 TTL=3 LOG_LEVEL='INFO' LOG_DATE_FORMAT='%Y-%m-%d,%H:%M:%S' LOG_FORMAT='[%(asctime)s.%(msecs)03d - %(levelname)s] %(filename)s:%(lineno)d | %(funcName)s - %(message)s' nose2