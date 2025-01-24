# Use an official Python runtime as a parent image
FROM python:3.10.13-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install necessary packages including Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev poppler-utils ffmpeg libsm6 libxext6 && \
    pip3 --no-cache-dir install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY src /app
COPY requirements.txt /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Define default command
CMD ["python", "app.py"]