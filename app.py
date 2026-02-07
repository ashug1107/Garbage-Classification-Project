import os
import io
import requests
import numpy as np
import tensorflow as tf
from PIL import Image
import streamlit as st

# --- 1. MODEL CONFIGURATION & LOADING ---
# We load the model once and cache it so the app stays fast
MODEL_PATH = "garbage_classifier_efficientnetb0_model.keras"
CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

@st.cache_resource
def load_garbage_model():
    try:
        # Using compile=False to avoid version mismatch errors during load
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_garbage_model()

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) 
    return img_array

# --- 2. PAGE CONFIG & UI ---
st.set_page_config(page_title="EcoScan AI", page_icon="♻️", layout="wide")

# (Your existing CSS styling goes here - keep it exactly as you had it)
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    .hero-container {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 3rem; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(5, 150, 105, 0.2);
    }
    .hero-title { font-size: 3rem !important; font-weight: 800 !important; }
    .content-card {
        background: rgba(255, 255, 255, 0.9); padding: 2rem;
        border-radius: 15px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }
    .result-box {
        padding: 1.5rem; border-radius: 12px; background: #ecfdf5;
        border: 2px solid #10b981; text-align: center; margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">🍃 EcoScan AI</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Waste sorting powered by Computer Vision.</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. MAIN INTERFACE ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="content-card"><h3>📥 Input Source</h3>', unsafe_allow_html=True)
    src_tab = st.tabs(["📤 Upload", "📷 Camera"])
    final_img = None
    with src_tab[0]:
        up_file = st.file_uploader("Select image", type=['jpg','jpeg','png'])
        if up_file: final_img = up_file
    with src_tab[1]:
        cam_file = st.camera_input("Capture item")
        if cam_file: final_img = cam_file
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="content-card"><h3>🤖 AI Analysis</h3>', unsafe_allow_html=True)
    if final_img:
        st.image(Image.open(final_img), width=350)
        
        if st.button("🚀 Run Analysis"):
            if model is None:
                st.error("Model not loaded. Check logs.")
            else:
                with st.spinner("Analyzing..."):
                    # INTERNAL PREDICTION (No API call needed!)
                    img_bytes = final_img.getvalue()
                    processed = preprocess_image(img_bytes)
                    predictions = model.predict(processed)
                    
                    pred_idx = np.argmax(predictions[0])
                    label = CLASS_NAMES[pred_idx].upper()
                    conf = float(np.max(predictions[0]))

                    st.markdown(f"""
                        <div class="result-box">
                            <p style="margin:0; color:#065f46;">PREDICTED CATEGORY</p>
                            <h2 style="margin:0; color:#059669;">{label}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    st.write(f"**Confidence:** {conf*100:.1f}%")
                    st.session_state['last_pred'] = label.lower()
    else:
        st.info("Upload an image to start.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. FEEDBACK (GITHUB ISSUES) ---
if 'last_pred' in st.session_state:
    st.markdown('<div class="content-card"><h3>🛠️ Feedback</h3>', unsafe_allow_html=True)
    correct_cat = st.selectbox("Correct Category:", CLASS_NAMES)
    if st.button("📩 Report Mismatch"):
        # We still use requests for the GitHub API part
        GITHUB_TOKEN = "github_pat_..." 
        REPO_OWNER = "ashug1107"
        REPO_NAME = "Garbage-Classification-Project"
        
        issue_payload = {
            "title": f"Mismatched Classification: {st.session_state['last_pred']} vs {correct_cat}",
            "body": f"Reported via EcoScan App UI.",
            "labels": ["bug"]
        }
        res = requests.post(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues", 
                            json=issue_payload, 
                            headers={"Authorization": f"token {GITHUB_TOKEN}"})
        if res.status_code == 201: st.success("Logged to GitHub!")
    st.markdown('</div>', unsafe_allow_html=True)
