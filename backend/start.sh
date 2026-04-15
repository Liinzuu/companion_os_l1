#!/bin/sh
# Companion OS — production start script
# Runs migrations then starts gunicorn.
# This is a single script so Railway's startCommand is one command (no && chain issues).

echo "=== Running migrations ==="
python manage.py migrate --noinput

# Create superuser if DJANGO_SUPERUSER_USERNAME is set and user doesn't exist yet.
# Uses Django's built-in --noinput flag which reads from environment variables.
# Safe to run on every deploy — does nothing if user already exists.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
    echo "=== Checking superuser ==="
    python manage.py createsuperuser --noinput 2>/dev/null || echo "Superuser already exists"
fi

echo "=== Starting gunicorn on port $PORT ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 1
