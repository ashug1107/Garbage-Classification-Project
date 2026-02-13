# Use 'bullseye-slim' instead of just 'slim' for stability
FROM python:3.11-bullseye

# Ensure we have root permissions
USER root

# Clean and update using a more stable repository approach
RUN apt-get clean && \
    apt-get update && \
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
RUN chmod +x run.sh
EXPOSE 10000
CMD ["./run.sh"]



