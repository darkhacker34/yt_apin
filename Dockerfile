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
RUN pip install --no-cache-dir flask yt-dlp requests

# Expose port 5000 (Flask's default port)
EXPOSE 5000

# Set environment variable to ensure Flask runs in production mode
ENV FLASK_APP=yt_api.py
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
