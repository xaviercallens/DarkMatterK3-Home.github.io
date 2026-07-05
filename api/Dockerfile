FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_dispatcher.py .

CMD ["uvicorn", "api_dispatcher:app", "--host", "0.0.0.0", "--port", "8080"]
