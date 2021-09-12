#!/usr/bin/env bash

python /app/src/manage.py migrate --noinput \
&& uvicorn antares.asgi:application --host 0.0.0.0 --port 8000
