#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn cyclon_project.wsgi:application --bind 0.0.0.0:5000 --workers 1 --timeout 90