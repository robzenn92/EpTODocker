#!/usr/bin/env bash

echo "Running tests."
sh run_tests.sh
if [ $? -eq 0 ]; then
    echo "Building Cyclon.."
    sh ./cyclon/build.sh
    echo "Building EpTO.."
    sh ./epto/build.sh
fi