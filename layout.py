import streamlit as st

def create_sidebar():
    # Sidebar for model selection and settings
    st.sidebar.title("Settings")
    
    model_options = ["Claude 3 Opus", "Claude 3 Sonnet", "Claude 3 Haiku"]
    model_name = st.sidebar.selectbox("Choose a model", model_options, key="model_name")

    max_tokens = st.sidebar.slider("Max Tokens", min_value=0, max_value=4096, value=256, step=256, key="max_tokens")
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.9, step=0.1, key="temperature")

def create_main_area():
    st.title("PDF Text Summarizer with Claude 3 LLM")
    
    # Reset button
    if st.button("Reset"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
    
    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    return uploaded_file

def create_output_area(summary):
    st.header("Output")
    if summary:
        st.write("Summary:")
        st.write(summary)
        
        # Save options
        st.write("Save the summary:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Save as TXT"):
                with open("summary.txt", "w") as file:
                    file.write(summary)
                with open("summary.txt", "r") as file:
                    st.download_button(label="Download TXT", data=file, file_name="summary.txt", mime="text/plain")
        with col2:
            if st.button("Save as CSV"):
                with open("summary.csv", "w") as file:
                    file.write(summary)
                with open("summary.csv", "r") as file:
                    st.download_button(label="Download CSV", data=file, file_name="summary.csv", mime="text/csv")
        with col3:
            if st.button("Save as DOC"):
                with open("summary.docx", "w") as file:
                    file.write(summary)
                with open("summary.docx", "rb") as file:
                    st.download_button(label="Download DOC", data=file, file_name="summary.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        with col4:
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
