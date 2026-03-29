import streamlit as st
import base64
import os
import time

# ---------- LOAD IMAGE ----------
def get_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE_DIR = os.path.dirname(__file__)
bg_path = os.path.join(BASE_DIR, "assets", "background.jpg")
bg_image = get_base64(bg_path)

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Agriculture", page_icon="🌾", layout="wide")

# ---------- CSS ----------
st.markdown(f"""
<style>

/* 🌌 Background */
[data-testid="stAppViewContainer"] {{
    background: url("data:image/jpg;base64,{bg_image}") no-repeat center center fixed;
    background-size: cover;
}}

/* 🌫️ Blur overlay */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    inset: 0;
    backdrop-filter: blur(10px);
    background: linear-gradient(to bottom, rgba(0,0,0,0.6), rgba(0,0,0,0.4));
    z-index: 0;
}}

[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}

/* 🔹 Transparent header */
header[data-testid="stHeader"] {{
    background: transparent;
}}

/* 🔹 Sidebar glass */
[data-testid="stSidebar"] {{
    background: rgba(0,0,0,0.3);
    backdrop-filter: blur(12px);
}}

/* 🔹 Sidebar text */
[data-testid="stSidebar"] * {{
    color: white !important;
}}

/* 🌟 Glass card */
.glass {{
    background: rgba(255,255,255,0.1);
    padding: 50px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    text-align: center;
    color: white;
    animation: fadeIn 1.5s ease;
}}

/* 🔥 Title */
.title {{
    font-size: 55px;
    font-weight: 700;
}}

/* ✨ Subtitle */
.subtitle {{
    font-size: 18px;
    opacity: 0.8;
}}

/* 🚀 Button */
.stButton > button {{
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white;
    border-radius: 25px;
    padding: 14px 30px;
    font-size: 16px;
    border: none;
    transition: 0.4s;
}}

.stButton > button:hover {{
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(255,75,43,0.8);
}}

/* ✨ Feature Section */
.section-title {{
    text-align: center;
    color: white;
    font-size: 30px;
    margin-top: 50px;
}}

/* ✨ Feature cards */
.card {{
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align:center;
    color:white;
    transition:0.3s;
}}

.card:hover {{
    transform: translateY(-10px);
    background: rgba(255,255,255,0.15);
}}

/* ✨ Animation */
@keyframes fadeIn {{
    from {{opacity:0; transform: translateY(40px);}}
    to {{opacity:1;}}
}}

</style>
""", unsafe_allow_html=True)

# ---------- TYPING EFFECT ----------
title_placeholder = st.empty()
full_text = "🌾 Sasya Netra"

for i in range(len(full_text)+1):
    title_placeholder.markdown(
        f"<h1 style='text-align:center; color:white;'>{full_text[:i]}</h1>",
        unsafe_allow_html=True
    )
    time.sleep(0.03)

# ---------- CENTER CONTENT ----------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("""
    <div class="glass">
        <p class="subtitle">
        Detect crop diseases using uploading images, voice, and live camera.<br>
        Empower farmers with smart technology.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 Start Detection"):
        st.switch_page("pages/app.py")

# ---------- FEATURES SECTION ----------
st.markdown("<h2 class='section-title'>🚀 Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>📸 Image Detection</h3>
    <p>Upload crop images to detect diseases instantly.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>🎤 Voice Input</h3>
    <p>Describe your crop problem using voice.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>📸 Live Camera</h3>
    <p>Capture crop images in real-time using your camera.</p>
    </div>
    """, unsafe_allow_html=True)