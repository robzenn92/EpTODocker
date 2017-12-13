#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
export VIEW_LIMIT='4'
export SHUFFLE_LENGTH='3'
export BROADCAST_PROB='0.5'
export FANOUT='2'
export TTL='3'
export LOG_LEVEL='INFO'
export LOG_DATE_FORMAT='%Y-%m-%d,%H:%M:%S'
export LOG_FORMAT='[%(asctime)s.%(msecs)03d - %(levelname)s] %(filename)s:%(lineno)d | %(funcName)s - %(message)s'
exec gunicorn epto_project.wsgi:application --bind 0.0.0.0:5001 --workers 1 --threads 3