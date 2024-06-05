import streamlit as st
from utils import reload_page, generate_unique_filename

from config_anthropic_claude3 import DEFAULT_MODEL_NAME as CLAUDE_MODEL
from config_openai_gpt4o import DEFAULT_MODEL_NAME as GPT4O_MODEL

def create_sidebar():
    st.sidebar.title("Settings")
    
    api_provider = st.sidebar.selectbox("Choose API Provider", ["Anthropic Claude 3", "OpenAI GPT-4o"], key="api_provider")
    
    if api_provider == "Anthropic Claude 3":
        model_options = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
        model_name = st.sidebar.selectbox("Choose Claude Model", model_options, key="model_name")
        max_tokens = st.sidebar.slider("Max Tokens", min_value=0, max_value=4096, step=256, key="max_tokens")
        temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, key="temperature")
    elif api_provider == "OpenAI GPT-4o":
        model_name = GPT4O_MODEL
        max_tokens = st.sidebar.slider("Max Tokens", min_value=0, max_value=4096, step=256, key="max_tokens")
        temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, key="temperature")
        top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, step=0.1, key="top_p")
        frequency_penalty = st.sidebar.slider("Frequency Penalty", min_value=0.0, max_value=2.0, step=0.1, key="frequency_penalty")
        presence_penalty = st.sidebar.slider("Presence Penalty", min_value=0.0, max_value=2.0, step=0.1, key="presence_penalty")
    
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
        
        st.markdown(summary)
        st.divider()
        
        # Display the summary using markdown
        with st.expander("Copy to Clipboard"):
            st.code(summary, language='markdown', line_numbers=True)

        with st.expander("Save and Send Options"):
            # Save options
            st.write("Save the summary:")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Save as TXT"):
                    filename = generate_unique_filename("summary", "txt")
                    with open(filename, "w") as file:
                        file.write(summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download TXT", data=file, file_name=filename, mime="text/plain")
            with col2:
                if st.button("Save as CSV"):
                    filename = generate_unique_filename("summary", "csv")
                    with open(filename, "w") as file:
                        file.write(summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download CSV", data=file, file_name=filename, mime="text/csv")
            with col3:
                if st.button("Save as DOC"):
                    filename = generate_unique_filename("summary", "docx")
                    with open(filename, "w") as file:
                        file.write(summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download DOC", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            with col4:
                if st.button("Save as XLS"):
                    filename = generate_unique_filename("summary", "xlsx")
                    with open(filename, "w") as file:
                        file.write(summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download XLS", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            # Email option
            st.write("Send the summary via email:")
            email_address = st.text_input("Email address")
            if st.button("Send Email"):
                send_email("Summary from Claude 3 LLM", summary, email_address, st.secrets["email"], st.secrets["email_password"])
