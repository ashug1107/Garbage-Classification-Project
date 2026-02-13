FROM python:3.11-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# THE FIX: Force install to the global system path
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir fastapi uvicorn streamlit python-multipart
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x run.sh
EXPOSE 10000
CMD ["./run.sh"]






