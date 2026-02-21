# Start backend on 8000 (internal)
uvicorn main:app --host 127.0.0.1 --port 8000 &
# Start frontend on Render's required $PORT (external)
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
