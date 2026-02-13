FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# IMPORTANT: Explicitly upgrade pip first
RUN python -m pip install --upgrade pip

# Copy requirements
COPY requirements.txt .

# FORCE installation of uvicorn and streamlit even if they are in requirements.txt
# This ensures they are in the PATH
RUN python -m pip install --no-cache-dir uvicorn streamlit
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the script is executable
RUN chmod +x run.sh

EXPOSE 10000

CMD ["./run.sh"]




