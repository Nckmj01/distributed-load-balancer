FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY load_balancer .

COPY hashing ./hashing

CMD ["python", "app.py"]
