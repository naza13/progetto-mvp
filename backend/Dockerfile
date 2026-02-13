FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Espone la porta dinamica di Cloud Run con fallback 8080
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}