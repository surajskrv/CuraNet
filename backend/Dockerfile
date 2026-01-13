FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY . /app/backend

EXPOSE 5000

CMD ["python", "-m", "backend.app"]
