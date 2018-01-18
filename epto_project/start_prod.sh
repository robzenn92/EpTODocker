#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn epto_project.wsgi:application --bind 0.0.0.0:5001 --workers 1