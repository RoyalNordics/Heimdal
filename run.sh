#!/bin/bash

# Start Gunicorn direkte uden at prøve at installere pakker igen
exec /opt/render/project/src/.venv/bin/gunicorn -b 0.0.0.0:$PORT webhook:app