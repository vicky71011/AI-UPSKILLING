FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY config ./config

RUN python -m pip install --no-cache-dir .

ENV DEFAULT_INPUT_FILE=/app/data/tickets.json

RUN useradd --create-home --uid 10001 appuser

USER appuser

ENTRYPOINT ["ticket-intelligence"]
CMD []