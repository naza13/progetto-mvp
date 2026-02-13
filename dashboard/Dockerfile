FROM python:3.11-slim
WORKDIR /app
COPY config.py .
COPY dashboard/requirements.txt .
COPY dashboard/app.py .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]