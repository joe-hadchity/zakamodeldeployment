# Use official Python image
FROM python:3.11-slim

# System packages required by OpenCV/YOLO
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libsm6 \
    libxrender1 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose Render’s port
EXPOSE 8080

# Run with Gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
