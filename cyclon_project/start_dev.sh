#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
export MY_POD_IP='lol'
export VIEW_LIMIT='4'
export SHUFFLE_LENGTH='3'
export LOG_LEVEL='INFO'
export LOG_DATE_FORMAT='%Y-%m-%d,%H:%M:%S'
export LOG_FORMAT='[%(asctime)s.%(msecs)03d] %(message)s' #[%(levelname)s] [%(filename)s:%(lineno)d] [%(funcName)s]
exec gunicorn cyclon_project.wsgi:application --bind 0.0.0.0:5000 --workers 1 --threads 3