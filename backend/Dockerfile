FROM python:3.11-slim
WORKDIR /app
COPY requirements.cloud.txt .
RUN pip install --no-cache-dir -r requirements.cloud.txt
COPY app.py .
ENV PORT=3000
EXPOSE 3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
