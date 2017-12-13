#!/usr/bin/env bash

echo "Checking Minikube Status"
minikube status > /dev/null
if [ $? -eq 1 ]; then
    echo "Minikube status was Stopped. It' will start in a while."
    minikube start
fi
#echo "Running tests."
#sh run_tests.sh
#if [ $? -eq 0 ]; then
    echo "Building Cyclon.."
    sh cyclon_project/build.sh
#    echo "Building EpTO.."
#    sh epto/build.sh
#fi