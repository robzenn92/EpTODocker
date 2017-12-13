#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
MY_POD_IP='lol' VIEW_LIMIT='4' SHUFFLE_LENGTH='3' LOG_LEVEL='INFO' LOG_DATE_FORMAT='%Y-%m-%d,%H:%M:%S' LOG_FORMAT='[%(asctime)s.%(msecs)03d - %(levelname)s] %(filename)s:%(lineno)d | %(funcName)s - %(message)s' exec gunicorn cyclon_project.wsgi:application --bind 0.0.0.0:5000 --workers 1 --threads 3