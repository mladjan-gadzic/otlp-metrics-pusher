FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp

COPY app.py .

CMD ["python", "-u", "app.py"]