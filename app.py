import streamlit as st
from app import generate_post, generate_batch

# -------------------------------
# ⚙️ PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Content System", layout="wide")

# -------------------------------
# 🎨 GLOBAL CSS (HARD OVERRIDE)
# -------------------------------
st.markdown("""
<style>

/* ===== ROOT BACKGROUND ===== */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #334155, #475569, #1e293b, #60a5fa) !important;
    background-size: 400% 400% !important;
    animation: gradientMove 12s ease infinite !important;
}

/* Animation */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===== REMOVE WHITE BACKGROUNDS SAFELY ===== */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stSidebar"] {
    background: transparent !important;
}

/* IMPORTANT: do NOT target all divs */

/* ===== TEXT ===== */
* {
    color: white !important;
}

/* ===== INPUTS ===== */
textarea, input {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
}

/* ===== SLIDER FIX ===== */
[data-testid="stSlider"] {
    pointer-events: auto !important;
}

[data-testid="stSlider"] div {
    pointer-events: auto !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    border-radius: 10px;
    font-size: 16px;
    cursor: pointer;
}

/* ===== OUTPUT CARD ===== */
.result-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)
# -------------------------------
# 🚀 HEADER
# -------------------------------
st.title("🚀 AI Content Lifecycle System")
st.markdown("Generate, optimize & translate LinkedIn content instantly")

st.markdown("---")

# -------------------------------
# 📥 INPUTS (NO CUSTOM CARD = NO BUG)
# -------------------------------
topic = st.text_area("📌 Enter Topic", placeholder="e.g. EVs in India")

col1, col2 = st.columns(2)

with col1:
    mode = st.selectbox("🎯 Tone", ["professional", "casual", "motivational"])

with col2:
    lang = st.selectbox("🌐 Language", ["both", "english", "hinglish"])

batch = st.slider("📦 Number of Posts", 1, 5, 1)

generate_btn = st.button("✨ Generate Content")

# -------------------------------
# 📤 OUTPUT
# -------------------------------
if generate_btn:

    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic")

    else:
        with st.spinner("Generating... 🚀"):
            results = generate_batch(topic, mode, lang, batch) if batch > 1 else [generate_post(topic, mode, lang)]

        st.success("✅ Done!")

        for i, result in enumerate(results):

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown(f"### 📄 Post {i+1}")
            st.write("**Status:**", result["status"])

            if "content" in result:
                st.markdown("#### 📌 English")
                st.write(result["content"])

            if "hinglish" in result:
                st.markdown("#### 🇮🇳 Hinglish")
                st.write(result["hinglish"])

            st.markdown('</div>', unsafe_allow_html=True)
