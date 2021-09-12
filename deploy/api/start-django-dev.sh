#!/usr/bin/env bash

python /app/src/manage.py migrate --noinput \
&& python /app/src/manage.py runserver 0.0.0.0:8000
