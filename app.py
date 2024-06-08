import streamlit as st
import os

from templates import prompt_templates
from utils import reload_page
from layout import create_sidebar, create_main_area, create_output_area, handle_uploaded_file, handle_url_input, handle_template_selection
from config import initialize_session_state, create_sidebar as config_create_sidebar
from api_helpers import initialize_clients, generate_summary
from youtube_api import handle_youtube_input, handle_language_selection

# Set environment variables
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]
os.environ["ANTHROPIC_API_KEY"] = st.secrets["anthropic"]["api_key"]
os.environ["GOOGLE_API_KEY"] = st.secrets["google"]["api_key"]

# Initialize the clients
openai_client, claude_client, genai = initialize_clients()

# Initialize session state variables
initialize_session_state()

# Sidebar settings
config_create_sidebar()

# Create main area
tab1, tab2, tab3 = st.tabs(["Upload", "URL", "YouTube"])
uploaded_file, url_input, submit_url, youtube_input, submit_youtube = None, None, None, None, None

with tab1:
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"], key="file_uploader")

with tab2:
    url_input = st.text_input("Enter URL", key="url_input")
    submit_url = st.button("Submit URL", key="submit_url")

with tab3:
    youtube_input = st.text_input("Enter YouTube URL or ID", key="youtube_input")
    submit_youtube = st.button("Submit URL or ID", key="submit_youtube")

# Handle uploaded file
handle_uploaded_file(uploaded_file)

# Handle URL input
handle_url_input(url_input, submit_url)

# Check for YouTube or ID input or submit button
if youtube_input and submit_youtube:
    handle_youtube_input(youtube_input)
    st.session_state['active_tab'] = 'YouTube'

# Handle language selection for YouTube transcript
handle_language_selection()

# Debugging: Überprüfen der Daten im Session State
st.write(f"Session State: {st.session_state}")

if "text" in st.session_state.data and st.session_state.data["text"]:
    with st.expander(f"Extracted Text (Word count: {st.session_state.data['word_count']}):"):
        st.write(st.session_state.data["text"][:2000])  # Display the first 2000 characters

# Handle template selection and prompt editing
prompt = handle_template_selection(prompt_templates)

# API call and response handling
if st.button("Generate Summary"):
    prompt_with_text = st.session_state.settings["prompt"].replace("{text}", st.session_state.data["text"])

    with st.spinner("Generating summary..."):
        try:
            summary, model_used = generate_summary(
                openai_client,
                claude_client,
                st.session_state.settings["model_name"],
                prompt_with_text,
                st.session_state.settings["temperature"],
                st.session_state.settings["max_tokens"],
                st.session_state.settings["api_provider_index"]
            )
            st.session_state.data["summary"] = summary
            st.session_state.data["model_used"] = model_used

        except Exception as e:
            st.session_state.data["summary"] = f"An error occurred during the API call: {str(e)}"
            st.session_state.data["model_used"] = ""

# Create the output area
if "summary" in st.session_state.data:
    create_output_area(
        st.session_state.data["summary"],
        st.session_state.data.get("model_used", "")
    )
