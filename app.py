import streamlit as st
import os
import io
import json
import zipfile
import requests
import numpy as np
from PIL import Image

# --- 1. CORE CONFIGURATION & VERSION FIX ---
# This MUST be set before importing tensorflow/keras
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tensorflow as tf
import tf_keras as keras

# GitHub Credentials (Use Environment Variables on Render for security!)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "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") 
REPO_OWNER = "ashug1107"
REPO_NAME = "Garbage-Classification-Project"
CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# --- 2. DEEP SURGERY MODEL LOADING ---
@st.cache_resource
def load_model_integrated():
    model_path = "garbage_classifier_efficientnetb0_model.keras"
    try:
        # Step A: Perform Surgery on the config
        with zipfile.ZipFile(model_path, 'r') as zip_ref:
            config_str = zip_ref.read('config.json').decode('utf-8')
        
        config_str = config_str.replace('"batch_shape"', '"batch_input_shape"')
        target_dtype_block = '"dtype": {"module": "keras", "class_name": "DTypePolicy", "config": {"name": "float32"}, "registered_name": null}'
        config_str = config_str.replace(target_dtype_block, '"dtype": "float32"')

        # Step B: Rebuild & Load Weights
        config_dict = json.loads(config_str)
        model = keras.models.model_from_json(json.dumps(config_dict))
        model.load_weights(model_path)
        return model
    except Exception as e:
        st.error(f"Model Surgery Failed: {e}")
        return None

# --- 3. PAGE SETUP & UI ---
st.set_page_config(page_title="EcoScan AI", page_icon="♻️", layout="wide")

# (Insert your existing CSS block here - omitted for brevity)
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# Load the model
model = load_model_integrated()

# --- 4. PREDICTION LOGIC ---
def process_and_predict(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB').resize((224, 224))
    img_array = tf.keras.utils.img_to_array(img) / 255.0  # Normalize if needed
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    idx = np.argmax(predictions[0])
    conf = float(np.max(predictions[0]))
    return CLASS_NAMES[idx], conf

# --- 5. GITHUB REPORTING LOGIC ---
def report_to_github(predicted, actual):
    github_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {
        "title": f"Mismatched Classification: {predicted} vs {actual}",
        "body": f"### Report\n- Predicted: `{predicted}`\n- Actual: `{actual}`",
        "labels": ["bug"]
    }
    return requests.post(github_url, json=payload, headers=headers)

# --- 6. MAIN INTERFACE ---
st.markdown('<div class="hero-container"><h1 class="hero-title">🍃 EcoScan AI</h1></div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.info("Step 1: Provide a photo.")
    src_tab = st.tabs(["📤 Upload", "📷 Camera"])
    final_img_data = None
    with src_tab[0]:
        up = st.file_uploader("Select image", type=['jpg','jpeg','png'], label_visibility="collapsed")
        if up: final_img_data = up.getvalue()
    with src_tab[1]:
        cam = st.camera_input("Capture", label_visibility="collapsed")
        if cam: final_img_data = cam.getvalue()

with col_right:
    if final_img_data:
        st.image(final_img_data, width=400)
        if st.button("🚀 Run AI Analysis"):
            with st.spinner("Analyzing..."):
                label, conf = process_and_predict(final_img_data)
                st.session_state['last_pred'] = label
                st.success(f"Prediction: {label.upper()} ({conf*100:.1f}%)")

# --- 7. FEEDBACK LOOP ---
if 'last_pred' in st.session_state:
    st.markdown("### 🛠️ Feedback & Refinement")
    correct_cat = st.selectbox("Actual Category:", CLASS_NAMES)
    if st.button("📩 Report Mismatch"):
        res = report_to_github(st.session_state['last_pred'], correct_cat)
        if res.status_code == 201:
            st.balloons()
            st.toast("Error logged to GitHub!")
        else:
            st.error("GitHub Sync Failed. Check Token.")
