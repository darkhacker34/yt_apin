FROM python:3.13-slim

WORKDIR /app
COPY main.py .
COPY cookies.txt .  # Add cookies file

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask yt-dlp requests gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
