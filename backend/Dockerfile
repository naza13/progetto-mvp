FROM python:3.11-slim
WORKDIR /app
COPY config.py .
COPY backend/requirements.txt .
COPY backend/main.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]