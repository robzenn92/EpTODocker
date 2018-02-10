#!/bin/bash

# Start Gunicorn processes
echo "Starting Gunicorn."
echo "Number of workers=${NUMBER_OF_WORKERS}."
echo "Number of threads=${NUMBER_OF_THREADS}."
exec gunicorn --bind 0.0.0.0:5001 --workers $NUMBER_OF_WORKERS --threads $NUMBER_OF_THREADS --timeout 90 epto_project.wsgi:application