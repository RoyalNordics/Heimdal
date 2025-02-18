#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start serveren med gunicorn
exec gunicorn -b 0.0.0.0:$PORT webhook:app