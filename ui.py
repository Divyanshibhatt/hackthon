from flask import app
import streamlit as st
from app import generate_post, generate_batch

# -------------------------------
# 🎨 PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI LinkedIn Generator",
    layout="centered"
)

# -------------------------------
# 🎨 CUSTOM CSS (White + Green + Animated Background)
# -------------------------------

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background-color: white;
        background-image: url("https://pixlr.com/images/generator/simple-generator.webp");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    /* Light overlay for readability */

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.85);
        z-index: -1;
    }

    /* Title styling */

    h1 {
        color: #0B6E4F;
        text-align: center;
        font-weight: bold;
    }

    /* Green button styling */

    .stButton > button {
        background-color: #28a745;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        transition: 0.3s;
    }

    .stButton > button:hover {
        background-color: #1e7e34;
        color: white;
    }

    /* Rounded inputs */

    textarea, input, select {
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# TITLE
# -------------------------------

st.title("🚀 AI Content Lifecycle System")
st.markdown("Generate LinkedIn posts with AI (English + Hinglish)")

st.markdown("---")

# -------------------------------
# INPUTS
# -------------------------------

topic = st.text_area(
    "📌 Enter Topic",
    placeholder="e.g. EVs in India"
)

mode = st.selectbox(
    "🎯 Select Tone",
    ["professional", "casual", "motivational"]
)

lang = st.selectbox(
    "🌐 Select Language",
    ["both", "english", "hinglish"]
)

batch = st.slider(
    "📦 Number of Posts",
    1,
    5,
    1
)

# -------------------------------
# BUTTON
# -------------------------------

if st.button("Generate Content"):

    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic")

    else:
        with st.spinner("Generating... 🚀"):

            if batch > 1:
                results = generate_batch(
                    topic,
                    mode,
                    lang,
                    batch
                )

            else:
                results = [
                    generate_post(
                        topic,
                        mode,
                        lang
                    )
                ]

        st.success("✅ Done!")

        # -------------------------------
        # OUTPUT
        # -------------------------------

        for i, result in enumerate(results):

            st.markdown(f"## 📄 Post {i+1}")

            st.write(
                "**Status:**",
                result["status"]
            )

            if "content" in result:
                with st.expander("📌 English Content"):
                    st.write(
                        result["content"]
                    )

            if "hinglish" in result:
                with st.expander("🇮🇳 Hinglish Content"):
                    st.write(
                        result["hinglish"]
                    )

            st.markdown("---")