# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt first (to leverage Docker cache)
COPY requirements.txt .

# Install system dependencies (optional, but sometimes needed)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Create and activate virtual environment
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip setuptools wheel gunicorn && \
    pip install -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD [ "/opt/venv/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app" ]
