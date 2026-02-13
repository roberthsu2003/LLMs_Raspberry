FROM python:3.11-slim

WORKDIR /app

COPY tools.py .

RUN pip install --no-cache-dir \
  mcpo \
  requests

EXPOSE 8000
