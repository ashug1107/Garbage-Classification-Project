# Use a lightweight Python 3.11 base
FROM python:3.11-slim

# Install system dependencies for OpenCV and TensorFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Make the start script executable
RUN chmod +x start.sh

# Render expects Port 10000 by default
EXPOSE 10000

# Start both services via our script
CMD ["./run.sh"]
