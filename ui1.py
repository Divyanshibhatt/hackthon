import streamlit as st
from app import generate_post
st.set_page_config(
    page_title="AI Content System",
    page_icon="🚀",
    layout="wide"
)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #334155, #475569, #1e293b, #60a5fa);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}
/* ☀️ Light mode override */
@media (prefers-color-scheme: light) {
    html, body, [data-testid="stAppViewContainer"] {
        background: #f8fafc !important;
    }
}

/* Animation */
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
/* 🔤 TEXT FIX */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #111827 !important;
}
/* 🧾 INPUTS */
textarea, input {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
/* 📦 RESULT CARD */
.result-card {
    background: #ffffff !important;
    color: #111827 !important;
    padding: 20px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

/* 🔽 EXPANDER */
details, summary {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 8px;
    padding: 6px;
}

/* 🔘 BUTTON */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white !important;
    border-radius: 10px;
    font-size: 16px;
}

/* Dropdown */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #111827 !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🖥️ HEADER
# -------------------------------
st.title("🚀 AI Content Lifecycle System")
st.markdown("Multi-Agent AI for LinkedIn Content Generation")
st.markdown("---")

# -------------------------------
# 🧾 INPUTS
# -------------------------------
topic = st.text_area(
    "📌 Enter Topic",
    placeholder="e.g. Future of AI in India",
    key="topic"
)

col1, col2 = st.columns(2)

with col1:
    mode = st.selectbox(
        "🎯 Tone",
        ["professional", "casual", "motivational"],
        key="mode"
    )

with col2:
    lang = st.selectbox(
        "🌐 Language",
        ["both", "english", "hinglish"],
        key="lang"
    )

batch = st.number_input(
    "📦 Number of Posts",
    min_value=1,
    max_value=10,
    value=1,
    key="batch"
)

length = st.selectbox(
    "📝 Post Length",
    ["short", "medium", "long"],
    key="length"
)
generate_btn = st.button("✨Generate Content")
if generate_btn:
    if topic.strip()=="":
        st.warning("⚠️Please enter a topic")
    else:
        with st.spinner("🤖 Agents are working..."):
            results = []
            for _ in range(batch):
                results.append(generate_post(topic, mode, lang, length))
        st.success("✅ Generated with Multi-Agent AI System")
        for i, r in enumerate(results):
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"### 📄 Post {i+1}")
            st.markdown(f"**Status:** {r.get('status', 'Approved')}")
            if "content" in r:
                with st.expander("📌 English"):
                    st.text_area(
                        "English Content",
                        value=r["content"],
                        height=200,
                        key=f"eng_{i}",
                        label_visibility="collapsed"
                    )
            if "hinglish" in r:
                with st.expander("📌 Hinglish"):
                    st.text_area(
                        "Hinglish Content",
                        value=r["hinglish"],
                        height=200,
                        key=f"hing_{i}",
                        label_visibility="collapsed"
                    )
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")
st.info("💡 Tip: Copy and post directly on LinkedIn for best engagement 🚀")
