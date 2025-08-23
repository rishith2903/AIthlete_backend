# Minimal Dockerfile for ML API server (runtime dependencies only)
FROM python:3.11-slim
WORKDIR /app
# Use a small runtime requirements file to avoid heavy build-time dependencies
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt
COPY . /app
EXPOSE 5000
CMD ["python", "api_server.py"]
