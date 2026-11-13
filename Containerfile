FROM docker.io/library/python:3.15.2-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV HOST=0.0.0.0 DATABASE_PATH=/data/message.db
CMD ["python", "app.py"]
