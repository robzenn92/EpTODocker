#!/usr/bin/env bash

export PYTHONPATH='.'

# Install requirements
pip install -r requirements.txt

# Run tests
sh run_tests.sh