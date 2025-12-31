FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Non-root user
RUN useradd -m -u 10001 appuser

# Dependencies first (better caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# App source (secrets excluded by .dockerignore)
COPY --chown=appuser:appuser . /app

USER appuser

CMD ["python", "main.py"]

