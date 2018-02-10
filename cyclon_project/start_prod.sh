#!/bin/bash

# Start Gunicorn processes
echo "Starting Gunicorn."
echo "Number of workers=${NUMBER_OF_WORKERS}."
echo "Number of threads=${NUMBER_OF_THREADS}."
exec gunicorn --bind 0.0.0.0:5000 --workers $NUMBER_OF_WORKERS --threads $NUMBER_OF_THREADS --timeout 90 cyclon_project.wsgi:application