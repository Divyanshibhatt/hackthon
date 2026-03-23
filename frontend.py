import streamlit as st
import requests

# Page settings
st.set_page_config(
    page_title="AI Content Lifecycle System",
    layout="centered"
)

# Custom pastel green background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #DFFFD6;
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

st.header("Enter Topic for LinkedIn Post")

topic = st.text_input(
    "Describe the topic:",
    placeholder="Enter the topic for your LinkedIn post"
)

# -------------------------
# Generate Content
# -------------------------

if st.button("Generate Content"):

    if topic.strip() == "":
        st.warning("Please enter a topic before generating content.")

    else:
        with st.spinner("Generating content..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/process",
                    json={"topic": topic}
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state["content"] = data["content"]
                    st.session_state["hinglish"] = data["hinglish"]
                    st.session_state["status"] = data["status"]
                    st.session_state["issues"] = data["compliance_issues"]

                else:
                    st.error("Server error")

            except Exception as e:
                st.error(f"Backend error: {e}")

# -------------------------
# Show Results
# -------------------------

if "content" in st.session_state:

    st.header("Generated Content")

    st.subheader("English Post")

    st.text_area(
        "English Content",
        st.session_state["content"],
        height=200
    )

    st.subheader("Hinglish Post")

    st.text_area(
        "Hinglish Content",
        st.session_state["hinglish"],
        height=200
    )

    st.subheader("Compliance Status")

    st.success(st.session_state["status"])

    st.subheader("Compliance Issues")

    if len(st.session_state["issues"]) == 0:
        st.write("No issues found.")

    else:
        for issue in st.session_state["issues"]:
            st.write(f"- {issue}")