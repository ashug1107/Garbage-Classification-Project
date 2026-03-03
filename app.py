import streamlit as st
import os
import io
import json
import zipfile
import requests
import numpy as np
from PIL import Image

# --- 1. CORE CONFIG & VERSION FIX (From main.py) ---
os.environ["TF_USE_LEGACY_KERAS"] = "1" 
import tensorflow as tf
import tf_keras as keras

# --- 2. GLOBAL SETTINGS ---
MODEL_PATH = "garbage_classifier_efficientnetb0_model.keras"
CLASS_NAMES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "ashug1107"
REPO_NAME = "Garbage-Classification-Project"

# --- 3. MODEL SURGERY & LOADING (From main.py) ---
@st.cache_resource
def load_model_integrated():
    try:
        # 1. Create a fresh, empty version of your architecture
        # This bypasses the need to read the broken config.json entirely
        base_model = tf.keras.applications.EfficientNetB0(
            include_top=False, 
            weights=None, 
            input_shape=(224, 224, 3),
            pooling='avg'
        )
        
        # Rebuild specific top layers
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.5), 
            tf.keras.layers.Dense(6, activation='softmax')
        ])
        
        # 2. Load only the weights from .keras file
        # .keras files are just ZIPs; Keras can often extract weights even if config is 'unknown'
        model.load_weights(MODEL_PATH)
        
        print("✅ System: Safe Shell Loaded Successfully.")
        return model
    except Exception as e:
        st.error(f"❌ Safe Shell Failed: {e}")
        # Final fallback: If even that fails, we try a direct load with compile=False
        try:
            return tf.keras.models.load_model(MODEL_PATH, compile=False)
        except:
            return None

model = load_model_integrated()

# --- 4. PAGE CONFIG & THEME (Frontend)  ---
st.set_page_config(
    page_title="EcoScan AI | Intelligent Waste Sorting",
    page_icon="♻️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    .hero-container {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 3rem; border-radius: 20px; color: white; text-align: center;
        margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(5, 150, 105, 0.2);
    }
    .hero-title { font-size: 3rem !important; font-weight: 800 !important; margin-bottom: 0.5rem !important; }
    .content-card {
        background: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        height: 100%;
    }
    div.stButton > button:first-child {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #059669; color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    div.stButton > button:first-child:hover { background-color: #047857; transform: scale(1.02); }
    .result-box {
        padding: 1.5rem; border-radius: 12px; background: #ecfdf5;
        border: 2px solid #10b981; text-align: center; margin-top: 1rem;
    }
    div[data-baseweb="select"] { background-color: #ffffff !important; border: 2px solid #059669 !important; border-radius: 8px !important; }
    div[data-testid="stSelectbox"] label p { color: #1e293b !important; font-weight: bold !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. HELPER FUNCTIONS (Logic from main.py) ---
def perform_prediction(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB').resize((224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) 
    preds = model.predict(img_array)
    idx = np.argmax(preds[0])
    return CLASS_NAMES[idx], float(np.max(preds[0]))

def report_error_to_github(predicted, actual):
    github_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {
        "title": f"Mismatched Classification: {predicted} vs {actual}",
        "body": f"### Report\n- Predicted: `{predicted}`\n- Actual: `{actual}`",
        "labels": ["bug"]
    }
    return requests.post(github_url, json=payload, headers=headers)

# --- 6. MAIN INTERFACE (Your Frontend) ---
st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">🍃 EcoScan AI</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">
            Empowering a cleaner future through computer vision.
        </p>
    </div>
    """, unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    with st.container():
        st.markdown('<div class="content-card" style="border-left: 10px solid #ef4444; padding: 20px;"><h3 style="margin:0; color:#1e293b;">📥 Input Source</h3></div>', unsafe_allow_html=True)
        st.info("Step 1: Provide a clear photo of the waste item.")
        src_tab = st.tabs(["📤 Upload Image", "📷 Live Camera"])
        
        final_img = None
        with src_tab[0]:
            up_file = st.file_uploader("Select image", type=['jpg','jpeg','png'], label_visibility="collapsed")
            if up_file: final_img = up_file
        with src_tab[1]:
            cam_file = st.camera_input("Capture", label_visibility="collapsed")
            if cam_file: final_img = cam_file

with col_right:
    with st.container():
        st.markdown('<div class="content-card" style="border-left: 10px solid #ef4444; padding: 20px;"><h3 style="margin:0; color:#1e293b;">🤖 Intelligence Output</h3></div>', unsafe_allow_html=True)
        if final_img:
            st.image(Image.open(final_img), width=400, caption="Target Image")
            
            if st.button("🚀 Run AI Analysis"):
                with st.spinner("Processing through neural layers..."):
                    try:
                        # INTERNAL CALL (No requests.post needed!)
                        label, conf = perform_prediction(final_img.getvalue())
                        
                        st.markdown(f"""
                            <div class="result-box">
                                <p style="margin:0; color:#065f46; font-weight:bold;">PREDICTED CATEGORY</p>
                                <h2 style="margin:0; color:#059669;">{label.upper()}</h2>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.write(f"**Match Confidence:** {conf*100:.1f}%")
                        bar_color = "#10b981"
                        st.markdown(f"""<div style="width: 100%; background-color: #e2e8f0; border-radius: 10px; height: 12px;"><div style="width: {conf*100}%; background-color: {bar_color}; height: 12px; border-radius: 10px;"></div></div>""", unsafe_allow_html=True) 
                        st.session_state['last_pred'] = label.lower()
                        
                    except Exception as e:
                        st.error(f"Prediction Error: {e}")
        else:
            st.info("Awaiting input image to begin analysis...")

# --- 7. FEEDBACK LOOP ---
if 'last_pred' in st.session_state:
    st.write("")
    with st.container():
        st.markdown('<div class="content-card" style="border-left: 10px solid #ef4444; padding: 20px;"><h3 style="margin:0; color:#1e293b;">🛠️ Feedback & Refinement</h3></div>', unsafe_allow_html=True)
        st.write("**Was this prediction incorrect?** Select the actual category helps me retrain the model.")
        
        f_c1, f_c2 = st.columns([2, 1])
        with f_c1:
            correct_cat = st.selectbox("Actual Category:", CLASS_NAMES)
        with f_c2:
            if st.button("📩 Report Mismatch"):
                res = report_error_to_github(st.session_state['last_pred'], correct_cat)
                if res.status_code == 201:
                    st.balloons()
                    st.toast("Success! Error logged to GitHub.", icon="✅")
                else:
                    st.error(f"Failed to sync with GitHub. Error: {res.status_code}")

# --- 8. SIDEBAR ---
with st.sidebar:
    st.markdown("## 📊 System Overview")
    st.metric("Model Engine", "EfficientNet-B0")
    st.metric("Test Accuracy", "85.02%")
    st.info("The AI identifies 6 categories of waste.")
    markdown_list_string = ""
    for item in CLASS_NAMES:
        markdown_list_string += f"- {item}\n"

    # 3. Pass the formatted string to st.info()
    st.info(markdown_list_string)
