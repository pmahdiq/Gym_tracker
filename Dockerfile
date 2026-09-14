FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

WORKDIR /app/gym_tracker

ENV SECRET_KEY=django-insecure-build-only-key

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "-c", "gunicorn gym_tracker.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file -"]