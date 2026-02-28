# 1. Use the standard slim image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Skip the 'apt-get' system updates entirely to avoid Exit Code 100
# We only need these if we use OpenCV. Pillow doesn't need them!

# 4. Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your project files
COPY . .

# 6. Create the upload folder
RUN mkdir -p user_uploads

# 7. Start the app
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]
