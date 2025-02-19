#!/bin/bash

# Installer afhængigheder
pip install --upgrade pip
pip install -r requirements.txt

# Start Flask-serveren med Gunicorn (hvis middleware.py ligger i src/)
exec gunicorn --chdir src -b 0.0.0.0:$PORT middleware:app
