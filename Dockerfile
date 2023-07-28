# Use a specific Python version (3.8-alpine)
FROM python:3.8-alpine

# Set the working directory
WORKDIR /app

# Update packages and install dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    bash \
    git \
    postgresql-dev \
    postgresql-client && \
    rm -rf /var/cache/apk/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file to the working directory
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV ALEMBIC_CONFIG=/app/alembic.ini

# Expose the port
EXPOSE 8000

# Run the Alembic upgrade command and start the application
CMD alembic upgrade head && \
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
