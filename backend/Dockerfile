FROM python:3.10-slim

WORKDIR /app

# Copy requirements first
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend package exactly as-is
COPY backend backend

EXPOSE 5000

# Run EXACTLY like local
CMD ["python", "-m", "backend.app"]
