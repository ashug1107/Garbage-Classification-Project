#!/bin/bash

# Start FastAPI (Backend) in background
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

echo
sleep 30

# Start Streamlit (Frontend)
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
