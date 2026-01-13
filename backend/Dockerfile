FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend backend

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:app"]
