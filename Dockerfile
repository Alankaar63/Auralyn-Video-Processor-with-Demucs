# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies and system tools
RUN apt-get update && apt-get install -y \
        build-essential \
        ffmpeg \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user first
RUN useradd -ms /bin/bash appuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create uploads and outputs folders with correct ownership
RUN mkdir -p uploads outputs \
    && chown -R appuser:appuser uploads outputs \
    && chmod -R 755 uploads outputs

# Switch to non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Run the Python app
CMD ["python", "app.py"]



# Build the Docker image with a proper name
# docker build -t auralyn-video-processor:latest .

# Run the container with a descriptive name
# docker run --name auralyn-video-container -p 5000:5000 auralyn-video-processor:latest
