#!/usr/bin/env bash

export PYTHONPATH='.'
export VIEW_LIMIT=3
export SHUFFLE_LENGTH=2
export TTL=3
nose2 --with-coverage --coverage ball --coverage event --coverage message --coverage partialView --coverage-report html