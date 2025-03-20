# Use official Python 3.13 slim image as the base
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy your Flask app script to the container
COPY main.py .

# Install system dependencies (for yt-dlp and requests)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask yt-dlp requests gunicorn

# Expose port 8000
EXPOSE 8000

# Command to run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
