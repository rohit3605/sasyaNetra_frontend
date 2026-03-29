import streamlit as st
from PIL import Image
import whisper
from streamlit_mic_recorder import mic_recorder
import tempfile
import os
import base64
import subprocess
import requests

# ---------- AUDIO CONVERSION ----------
def convert_audio(input_path, output_path):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI in Agriculture",
    page_icon="🌾",
    layout="wide"
)

# ---------- BACKGROUND ----------
def get_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE_DIR = os.path.dirname(__file__)
bg_path = os.path.join(BASE_DIR, "..", "assets", "new_bg.jpg")
bg_image = get_base64(bg_path)

# ---------- CSS ----------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("data:image/jpg;base64,{bg_image}") no-repeat center center fixed;
    background-size: cover;
}}

[data-testid="stAppViewContainer"]::before {{
    content:"";
    position:absolute;
    inset:0;
    backdrop-filter: blur(6px);
    background: rgba(0,0,0,0.5);
    z-index:0;
}}

[data-testid="stAppViewContainer"] > .main {{
    position:relative;
    z-index:1;
}}

header[data-testid="stHeader"] {{
    background: transparent !important;
}}

[data-testid="stSidebar"] {{
    background: rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
}}

[data-testid="stSidebar"] * {{
    color:white !important;
}}

.card {{
    background: rgba(255,255,255,0.1);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    color:white;
}}

.header {{
    text-align:center;
    color:white;
    font-size:40px;
    font-weight:700;
}}

[data-testid="stFileUploader"] {{
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 15px;
}}

[data-testid="stFileUploaderDropzone"] {{
    background: transparent !important;
    border: 2px dashed rgba(255,255,255,0.3);
}}

[data-testid="stFileUploader"] * {{
    color: white !important;
}}

button {{
    border-radius: 30px !important;
    background: linear-gradient(45deg, #00ffcc, #0066ff) !important;
    color: white !important;
    border: none !important;
    padding: 8px 18px !important;
    transition: 0.3s;
}}

button:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0,255,204,0.8);
}}

.mic-container button {{
    background: linear-gradient(45deg, #ff416c, #ff4b2b) !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------- BACK BUTTON ----------
if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")

# ---------- HEADER ----------
st.markdown("<div class='header'>🌾 Crop Disease Detection</div>", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Choose Input Method")
option = st.sidebar.radio(
    "",
    ["📸 Upload Image", "📷 Live Camera", "🎤 Voice Input"]
)

# ================= IMAGE =================
if option == "📸 Upload Image":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📤 Upload Crop Image")

    uploaded_file = st.file_uploader("Upload crop image", type=["jpg","png","jpeg"])
    # ✅ ADD THIS FIX
    if uploaded_file is None:
        st.session_state.pop("result", None)
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

        if st.button("🔍 Detect Disease"):
            with st.spinner("Analyzing..."):
                response = requests.post(
                    "http://127.0.0.1:8000/predict-image",
                    files={"file": (uploaded_file.name, uploaded_file.getvalue(), "image/jpeg")}
                )
                print(response.status_code)
                print(response.text)

                data = response.json()
                 # ✅ store result
                st.session_state["result"] = data
    # ✅ SHOW RESULT ONLY ONCE
    if "result" in st.session_state:
        data = st.session_state["result"]
        if "disease" in data:
                label = data["disease"]
                confidence = data["confidence"]
                st.success(f"🦠 Disease: {label}")
                st.info(f"Confidence: {confidence:.2f}%")
                # 💊 Advice
                if "advice" in data:
                    st.markdown("### 💊 Advice")
                    st.write(data["advice"])

        else:
            st.error("❌ Backend Error")
            st.write(data)

    else:
        st.info("Please upload a crop image before detection.")

    st.markdown("</div>", unsafe_allow_html=True)


# ================= CAMERA =================
elif option == "📷 Live Camera":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📸 Capture Crop Image")

    camera_image = st.camera_input("Take a picture of the crop")

    if camera_image:
        image = Image.open(camera_image)
        st.image(image, use_column_width=True)

        if st.button("🔍 Detect Disease"):
            with st.spinner("Analyzing..."):
                response = requests.post(
                    "http://127.0.0.1:8000/predict-image",
                    files={"file": (camera_image.name, camera_image.getvalue(), "image/jpeg")}
                )

                data = response.json()
                label = data["disease"]
                confidence = data["confidence"]

            st.success(f"🦠 Disease: {label}")
            st.info(f"Confidence: {confidence:.2f}%")
            # 💊 Advice
            if "advice" in data:
                st.markdown("### 💊 Advice")
                st.write(data["advice"])

    else:
        st.info("Please capture an image before detection.")

    st.markdown("</div>", unsafe_allow_html=True)


# ================= VOICE =================
elif option == "🎤 Voice Input":

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🎤 Describe Your Crop Problem")

    language_option = st.radio("Select Language", ["Hindi", "Bengali", "English"])
    lang_code = {"Hindi":"hi","Bengali":"bn","English":"en"}[language_option]

    st.write("🎙️ Click below to record your voice:")

    st.markdown('<div class="mic-container">', unsafe_allow_html=True)

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop",
        just_once=True,
        use_container_width=False
    )

    st.markdown('</div>', unsafe_allow_html=True)
    # ✅ ADD HERE (IMPORTANT)
    if audio is None:
        st.session_state.pop("voice_text", None)
        st.session_state.pop("voice_result", None)
    # ---------- PROCESS AUDIO ----------
    if audio:
        st.success("Recording complete!")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio["bytes"])
            raw_path = temp_audio.name

        clean_path = raw_path.replace(".wav", "_clean.wav")
        convert_audio(raw_path, clean_path)

        with st.spinner("Processing audio..."):
            result = model.transcribe(clean_path, task="transcribe", fp16=False)

        # ✅ STORE TEXT IN SESSION
        st.session_state["voice_text"] = result["text"].strip().capitalize()

        st.success("📝 Converted Text:")
        st.write(st.session_state["voice_text"])
        st.caption(f"Detected Language: {result['language']}")

    # ---------- SHOW STORED TEXT ----------
    if "voice_text" in st.session_state:
        st.write("👉 You said:")
        st.write(st.session_state["voice_text"])

        # ---------- BUTTON ----------
        if st.button("🔍 Detect Disease from Voice"):
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze-text",
                        data={"text": st.session_state["voice_text"]}
                    )

                    data = response.json()

                    # ✅ STORE RESULT
                    st.session_state["voice_result"] = data

                except Exception as e:
                    st.error("❌ Request Failed")
                    st.write(str(e))

    # ---------- SHOW RESULT ----------
    if "voice_result" in st.session_state:
        data = st.session_state["voice_result"]

        if "result" in data:
            st.success(f"🦠 Result: {data['result']}")
            st.info(f"Confidence: {data['confidence']:.2f}%")
            # 💊 Advice
            if "advice" in data:
                st.markdown("### 💊 Advice")
                st.write(data["advice"])
        else:
            st.error("❌ Backend Error")
            st.write(data)

    st.markdown("</div>", unsafe_allow_html=True)