FROM python:3.9

# Disables the buffer for instant output of messages to stdout from processes.
ENV PYTHONUNBUFFERED=1

# Install poetry
RUN pip install poetry

WORKDIR /app/src

COPY pyproject.toml poetry.lock /app/src/

## Install app requires
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./ /app/src/

# Move scripts to /app
RUN find . -name '*.sh' -exec mv '{}' /app/ \;
