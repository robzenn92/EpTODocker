#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn --bind 0.0.0.0:5001 --workers 1 epto_project.wsgi:application