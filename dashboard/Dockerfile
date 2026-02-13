FROM python:3.11-slim

WORKDIR /app

# Copia config.py dalla root
COPY config.py .

# Copia i file del dashboard
COPY dashboard/requirements.txt .
COPY dashboard/app.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]