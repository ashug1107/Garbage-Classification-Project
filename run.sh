#!/bin/bash
# Run FastAPI on internal port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Run Streamlit on the PUBLIC port Render provides
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
