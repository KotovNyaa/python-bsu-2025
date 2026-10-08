FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app

RUN pip install --no-cache-dir flask gunicorn

COPY . /app

EXPOSE 5000

CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:${PORT:-5000} 'lab.web.app:create_app()'"]
