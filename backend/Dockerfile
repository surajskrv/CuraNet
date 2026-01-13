FROM python:3.10-slim

WORKDIR /app

# Ensure Python can find backend package
ENV PYTHONPATH=/app

# Install dependencies
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source
COPY backend backend

EXPOSE 5000

CMD ["python", "-m", "backend.app"]
