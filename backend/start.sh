#!/bin/sh
# Companion OS — production start script
# Runs migrations then starts gunicorn.
# This is a single script so Railway's startCommand is one command (no && chain issues).

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Starting gunicorn on port $PORT ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 1
