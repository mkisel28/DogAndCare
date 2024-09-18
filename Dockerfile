FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /var/log/django && \
    chown -R www-data:www-data /var/log/django

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry


RUN poetry config virtualenvs.create false 

RUN poetry install --no-interaction --no-ansi

COPY . .


EXPOSE 8000
