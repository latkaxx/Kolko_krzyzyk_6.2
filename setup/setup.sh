#!/bin/bash

PYTHON=python

# Check if python link is available
if ! command -v $PYTHON &> /dev/null; then
    PYTHON=python3
fi

# Check if python3 exists, if not then we have a problem
if ! command -v $PYTHON &> /dev/null; then
    echo "Python is not installed on this system."
    exit 1
fi

# Create and activate virtual environment
"$PYTHON" -m venv env

source ./env/bin/activate

# Install dependencies
$PYTHON -m pip install -r requirements.txt
