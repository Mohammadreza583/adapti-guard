FROM python:3.12-slim

WORKDIR /app
COPY requirements-core.txt .
RUN pip install --no-cache-dir -r requirements-core.txt
COPY . .
ENV PYTHONPATH=/app

# API keys must be provided at runtime via environment variables
CMD ["python", "experiments/EXP000_api_smoke/run.py"]
