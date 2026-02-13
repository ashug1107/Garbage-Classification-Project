#!/bin/bash

# Force the container to look in the local bin folder where pip might have put things
export PATH=$PATH:/home/app/.local/bin:/root/.local/bin

# Start FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for model
sleep 30

# Start Streamlit
python -m streamlit run app.py --server.port 10000 --server.address 0.0.0.0
