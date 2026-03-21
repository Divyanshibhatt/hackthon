import streamlit as st
import requests

# Page settings
st.set_page_config(
    page_title="AI Content Lifecycle System",
    layout="centered"
)

# Custom peach background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFB07C;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("AI Content Lifecycle System")

# -------------------------
# Input Section
# -------------------------

st.header("Enter Product Information")

product_info = st.text_area(
    "Describe your product:",
    height=150
)

# -------------------------
# Generate Content
# -------------------------

if st.button("Generate Content"):

    if product_info == "":
        st.warning("Please enter product information")

    else:
        with st.spinner("Generating content..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:5000/process",
                    json={
                        "product_info": product_info
                    }
                )

                data = response.json()

                st.session_state["content"] = data["generated_content"]
                st.session_state["translation"] = data["hindi_translation"]
                st.session_state["status"] = data["status"]
                st.session_state["issues"] = data["compliance_issues"]

            except:
                st.error("Backend not running")

# -------------------------
# Show Results
# -------------------------

if "content" in st.session_state:

    st.header("Generated Content")

    st.text_area(
        "Content",
        st.session_state["content"],
        height=200
    )

    st.subheader("Compliance Status")

    st.success(st.session_state["status"])

    st.subheader("Compliance Issues")

    if len(st.session_state["issues"]) == 0:
        st.write("No issues found")
    else:
        for issue in st.session_state["issues"]:
            st.write(issue)

    st.subheader("Hindi Translation")

    st.text_area(
        "Translation",
        st.session_state["translation"],
        height=200
    )

# -------------------------
# Optimize Content
# -------------------------

if "content" in st.session_state:

    if st.button("Optimize Content"):

        with st.spinner("Optimizing content..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:5000/optimize",
                    json={
                        "generated_content": st.session_state["content"],
                        "product_info": product_info
                    }
                )

                report = response.json()

                st.header("Optimization Report")

                st.json(report)

            except:
                st.error("Optimization failed")