# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

FROM python:3.11.3-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && pip install poetry==1.3.2

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false  \
    && poetry install --without dev

WORKDIR /app

COPY . .
