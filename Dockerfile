# Use 3.11-slim as our base
FROM python:3.11-slim

# Ensure we are the root user to perform updates
USER root

# Fix for Exit Code 100:
# 1. Clean up any broken cache first
# 2. Use --allow-releaseinfo-change to bypass repository mismatches
RUN apt-get clean && \
    apt-get update --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglvnd0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# The rest of your Dockerfile stays the same...
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x start.sh
EXPOSE 10000
CMD ["./start.sh"]

