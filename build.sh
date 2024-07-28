#!/usr/bin/env bash

echo "BUILD START"

set -o errexit  # exit on error

pip3 install --upgrade pip
pip3 install -r requirements.txt --no-cache-dir

python3 manage.py collectstatic --no-input

echo "BUILD END"
