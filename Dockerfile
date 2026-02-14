FROM python:3.11-bullseye

WORKDIR /app

#Install system dependencies for image processing (OpenCV/Pillow support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglvnd0 \
    && rm -rf /var/lib/apt/lists/*

#Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

COPY requirements.txt .

#Install the heaviest package ALONE first
RUN python -m pip install --no-cache-dir tensorflow-cpu==2.16.1

#THE FIX: Force install to the global system path
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir fastapi uvicorn streamlit python-multipart
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x run.sh
EXPOSE 10000
CMD ["./run.sh"]









