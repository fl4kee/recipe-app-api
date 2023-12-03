FROM python:3.9-alpine3.13

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# Set up virtual environment
RUN python -m venv /py
ENV PATH="/py/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install PostgreSQL client
RUN apk add --update --no-cache postgresql-client

# Install build dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev

# Install Python dependencies
RUN pip install -r /tmp/requirements.txt

# Install development dependencies if needed
ARG DEV=false
RUN if [ "$DEV" = "true" ]; then pip install -r /tmp/requirements.dev.txt; fi

# Clean up
RUN rm -rf /tmp && apk del .tmp-build-deps

# Create non-root user
RUN adduser --disabled-password --no-create-home django-user


ENV PATH="/py/bin:$PATH"

USER django-user
