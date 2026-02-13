# 1. Use Bullseye for stability (Fixes Exit Code 100)
FROM python:3.11-bullseye

WORKDIR /app

# 2. Robust Update & Install
# We add --fix-missing to handle any temporary network blips
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglvnd0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Upgrade pip and install requirements
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install --no-cache-dir uvicorn streamlit
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x run.sh
EXPOSE 10000
CMD ["./run.sh"]





