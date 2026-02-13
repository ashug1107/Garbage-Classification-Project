#!/bin/bash

# Start FastAPI (Backend)
# We use python3 -m to be absolutely certain we use the right path
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for model loading
echo "System: Waiting for AI Model to load..."
sleep 30

# Start Streamlit (Frontend)
python3 -m streamlit run app.py --server.port 10000 --server.address 0.0.0.0
