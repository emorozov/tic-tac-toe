#!/usr/bin/env bash

python /app/src/manage.py makemigrations --dry-run --check \
&& python /app/src/manage.py check --fail-level=WARNING \
&& pytest $@
