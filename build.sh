#!/bin/bash

# Build the project
echo "Building the project"
python3.11 -m pip install -r requirements.txt

# Migrations
echo "Making Migrations"
python3.11 manage.py makemigrations --noinput
python3.11 manage.py migrate --noinput

echo "Collecting Static Files"
python3.11 manage.py collectstatic --noinput --clear
