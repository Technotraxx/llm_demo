import streamlit as st
from utils import reload_page

def create_sidebar():
    # Sidebar for model selection and settings
    st.sidebar.title("Settings")
    
    model_options = ["Claude 3 Opus", "Claude 3 Sonnet", "Claude 3 Haiku"]
    model_name = st.sidebar.selectbox("Choose a model", model_options, key="model_name")

    max_tokens = st.sidebar.slider("Max Tokens", min_value=0, max_value=4096, step=256, key="max_tokens")
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, key="temperature")

    # Reset button
    if st.sidebar.button("Reset"):
        reload_page()  # Reload the page

def create_main_area():
    st.title("PDF Text Summarizer with Claude 3 LLM")
    
    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    return uploaded_file

def create_output_area(summary):
    if summary:
        st.header("Output")
        st.write("Summary:")
        st.write(summary)

def create_right_sidebar(summary):
    with st.sidebar:
        st.header("Save and Send Options")
        if summary:
            # Save options
            st.write("Save the summary:")
            if st.button("Save as TXT"):
                with open("summary.txt", "w") as file:
                    file.write(summary)
                with open("summary.txt", "r") as file:
                    st.download_button(label="Download TXT", data=file, file_name="summary.txt", mime="text/plain")
            if st.button("Save as CSV"):
                with open("summary.csv", "w") as file:
                    file.write(summary)
                with open("summary.csv", "r") as file:
                    st.download_button(label="Download CSV", data=file, file_name="summary.csv", mime="text/csv")
            if st.button("Save as DOC"):
                with open("summary.docx", "w") as file:
                    file.write(summary)
                with open("summary.docx", "rb") as file:
                    st.download_button(label="Download DOC", data=file, file_name="summary.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            if st.button("Save as XLS"):
                with open("summary.xlsx", "w") as file:
                    file.write(summary)
                with open("summary.xlsx", "rb") as file:
                    st.download_button(label="Download XLS", data=file, file_name="summary.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            # Email option
            st.write("Send the summary via email:")
            email_address = st.text_input("Email address")
            if st.button("Send Email"):
                send_email("Summary from Claude 3 LLM", summary, email_address, st.secrets["email"], st.secrets["email_password"])
