# 1. Use a slim image to save memory (Crucial for Render Free Tier)
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install system dependencies for OpenCV/Pillow if needed
RUN apt-get clean && apt-get update --fix-missing && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy and install requirements first (to use Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your app (app.py and your .keras model)
COPY . .

# 6. Create the upload directory your code expects
RUN mkdir -p user_uploads

# 7. Use the $PORT variable provided by Render
# We don't use EXPOSE because Render assigns a random port
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]

