FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Add /app to PYTHONPATH so Python can find backend package
ENV PYTHONPATH=/app

# Copy requirements and install
COPY requirements.txt /app/backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code into /app/backend
COPY . /app/backend

# Expose Flask port
EXPOSE 5000

# Run as module (correct way)
CMD ["python", "-m", "backend.app"]
