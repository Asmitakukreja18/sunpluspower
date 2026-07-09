FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL client library
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and config files
COPY . .

# Create uploads folder inside the container
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Exec command (wait for database and apply migrations is handled via start command in docker-compose or script)
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
