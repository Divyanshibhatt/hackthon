import streamlit as st
import requests

# Page settings
st.set_page_config(
    page_title="AI Content Lifecycle System",
    layout="centered"
)

# Custom pastel green background
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #F9FAFB !important;
}

/* Force all text to dark */
html, body, [class*="css"] {
    color: #1E1E1E !important;
}

/* Fix input boxes */
input, textarea {
    background-color: white !important;
    color: black !important;
    border-radius: 8px !important;
}

/* Fix text areas (your output boxes) */
textarea {
    background-color: white !important;
    color: black !important;
}

/* Fix buttons */
button {
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Fix labels/headings visibility */
h1, h2, h3, h4, h5, h6, label, p {
    color: #1E1E1E !important;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("AI Content Lifecycle System")

# -------------------------
# Input Section
# -------------------------

st.header("Enter Topic ")

topic = st.text_input(
    "Describe the topic:",
    placeholder="Enter the topic "
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