import streamlit as st
from utils import reload_page, generate_unique_filename

def create_sidebar():
    # Sidebar for model selection und settings
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

        # Display the summary in a code block
        st.code(summary, language='text')
        
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
