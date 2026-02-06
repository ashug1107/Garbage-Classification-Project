import streamlit as st
import requests
from PIL import Image
import io

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="EcoScan AI | Intelligent Waste Sorting",
    page_icon="♻️",
    layout="wide"
)

# --- 2. BEAUTIFUL UI STYLING (CSS) ---
st.markdown("""
    <style>
    /* Background and Global Styles */
    .stApp {
        background-color: #f0f4f8;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(5, 150, 105, 0.2);
    }
    
    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }

    /* Glassmorphism Card */
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        height: 100%;
    }

    /* Modern Buttons */
    div.stButton > button:first-child {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #059669;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #047857;
        border: none;
        color: white;
        transform: scale(1.02);
    }

    /* Prediction Result Highlight */
    .result-box {
        padding: 1.5rem;
        border-radius: 12px;
        background: #ecfdf5;
        border: 2px solid #10b981;
        text-align: center;
        margin-top: 1rem;
    }
            
    /* This targets the dropdown container */
div[data-baseweb="select"] {
    background-color: #ffffff !important; /* Force white background */
    border: 2px solid #059669 !important; /* Emerald border */
    border-radius: 8px !important;
}

/* This targets the text inside the dropdown */
div[data-testid="stSelectbox"] label p {
    color: #1e293b !important; /* Deep Slate color */
    font-weight: bold !important;
    font-size: 1.1rem !important;
}

/* This highlights the text of the options */
div[role="listbox"] ul li {
    color: #0f172a !important;
    font-weight: 500 !important;
}

    </style>
    """, unsafe_allow_html=True)

# --- 3. UPDATED HERO CONTAINER (Heading Fix) ---
st.markdown(f"""
    <div class="hero-container">
        <h1 class="hero-title">🍃 EcoScan AI</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">
            Empowering a cleaner future through computer vision. 
            Upload or capture waste to identify recyclability instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    #st.markdown("### 📥 Input Source")
    # Wrap input in a styled container
    with st.container():
        st.markdown("""
        <div class="content-card" style="border-left: 10px solid #ef4444; padding: 20px;">
            <h3 style="margin:0; color:#1e293b;">📥 Input Source</h3>
            <p style="color:#64748b; margin-bottom:10px;">Select a method to provide an image.</p>
        </div>
    """, unsafe_allow_html=True)
        st.info("Step 1: Provide a clear photo of the waste item.")
        src_tab = st.tabs(["📤 Upload Image", "📷 Live Camera"])
        
        final_img = None
        with src_tab[0]:
            up_file = st.file_uploader("Select image file", type=['jpg','jpeg','png'], label_visibility="collapsed")
            if up_file: final_img = up_file
            
        with src_tab[1]:
            cam_file = st.camera_input("Capture item", label_visibility="collapsed")
            if cam_file: final_img = cam_file
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    #st.markdown("### 🤖 Intelligence Output")
    with st.container():
        st.markdown("""
        <div class="content-card" style="border-left: 10px solid #ef4444; padding: 20px;">
            <h3 style="margin:0; color:#1e293b;">🤖 Intelligence Output</h3>
            <p style="color:#64748b; margin-bottom:10px;">Select a method to provide an image.</p>
        </div>
    """, unsafe_allow_html=True)
        if final_img:
            st.image(Image.open(final_img), width=400, caption="Target Image")
            
            if st.button("🚀 Run AI Analysis"):
                with st.spinner("Processing through neural layers..."):
                    try:
                        # Call Backend
                        files = {"file": final_img.getvalue()}
                        res = requests.post("http://localhost:8000/predict", files=files)
                        
                        if res.status_code == 200:
                            data = res.json()
                            label = data["prediction"].upper()
                            conf = data["confidence"]
                            
                            st.markdown(f"""
                                <div class="result-box">
                                    <p style="margin:0; color:#065f46; font-weight:bold;">PREDICTED CATEGORY</p>
                                    <h2 style="margin:0; color:#059669;">{label}</h2>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Confidence display
                            st.write(f"**Match Confidence:** {conf*100:.1f}%")
                            #st.progress(conf)
                            # Create a custom colored bar that matches your theme
                            bar_color = "#10b981" # Emerald Green
                            st.markdown(f"""<div style="width: 100%; background-color: #e2e8f0; border-radius: 10px; height: 12px;"><div style="width: {conf*100}%; background-color: {bar_color}; height: 12px; border-radius: 10px; transition: width 0.5s ease-in-out;"></div></div>""", unsafe_allow_html=True)                   
                            st.session_state['last_pred'] = label.lower()
                        else:
                            st.error("Server Error: Backend is unreachable.")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")
        else:
            st.info("Awaiting input image to begin analysis...")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ENHANCED FEEDBACK LOOP ---
if 'last_pred' in st.session_state:
    st.write("")
    #st.markdown("### 🛠️ Feedback & Refinement")
    with st.container():
        st.markdown("""
        <div class="content-card" style="border-left: 10px solid #ef4444; padding: 20px;">
            <h3 style="margin:0; color:#1e293b;">🛠️ Feedback & Refinement</h3>
            <p style="color:#64748b; margin-bottom:10px;">Select the actual category helps me retrain the model.</p>
        </div>
    """, unsafe_allow_html=True)
        st.write("**Was this prediction incorrect?** Select the actual category helps me retrain the model.")
        
        f_c1, f_c2 = st.columns([2, 1])
        with f_c1:
            correct_cat = st.selectbox("Actual Category:", ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash'], label_visibility="visible")
        with f_c2:
            if st.button("📩 Report Mismatch"):
                try:
                    rep = requests.post("http://localhost:8000/report-error", 
                                       params={"predicted": st.session_state['last_pred'], "actual": correct_cat})
                    if rep.status_code == 200:
                        st.balloons()
                        st.toast("Success! Error logged to GitHub.", icon="✅")
                    else:
                        st.error("Failed to sync with GitHub.")
                except:
                    st.error("Backend Error.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. SIDEBAR SYSTEM INFO ---
with st.sidebar:
    st.markdown("## 📊 System Overview")
    st.markdown("---")
    st.metric("Model Engine", "EfficientNet-B0")
    st.metric("Test Accuracy", "89.44%")
    st.metric("Response Time", "< 0.5s")
    st.markdown("---")
    st.info("The AI identifies 6 categories of waste to optimize recycling sorting workflows.")