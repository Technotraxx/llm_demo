import streamlit as st
import os
import uuid

from templates import prompt_templates
from utils import (save_text, save_csv, save_doc, save_xls, send_email,
                   reload_page, generate_unique_filename, load_pdf, load_docx,
                   load_txt, load_csv, load_url)
from layout import create_sidebar as create_layout_sidebar, create_main_area, create_output_area
from config import initialize_session_state, create_sidebar
from api_helpers import get_gemini_response, initialize_clients
from youtube_api import process_youtube_input, load_youtube_transcript

# Set environment variables
os.environ["OPENAI_API_KEY"] = st.secrets["openai"]["api_key"]
os.environ["ANTHROPIC_API_KEY"] = st.secrets["anthropic"]["api_key"]
os.environ["GOOGLE_API_KEY"] = st.secrets["google"]["api_key"]

# Initialize the clients
openai_client, claude_client, genai = initialize_clients()

# Initialize session state variables
initialize_session_state()

# Sidebar settings
create_sidebar()

# Create main area
uploaded_file, url_input, submit_url, youtube_input, submit_youtube = create_main_area()

# Initialize active_tab in session state if not present
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = 'Upload'  # Default to the 'Upload' tab

# Function to simulate tab switching 
def display_active_tab():
    if st.session_state['active_tab'] == 'Upload':
        if uploaded_file:
            file_type = uploaded_file.name.split('.')[-1].lower()
            if file_type == 'pdf':
                text, word_count = load_pdf(uploaded_file)
            elif file_type == 'docx':
                text, word_count = load_docx(uploaded_file)
            elif file_type == 'txt':
                text, word_count = load_txt(uploaded_file)
            elif file_type == 'csv':
                text, word_count = load_csv(uploaded_file)
            
            st.session_state.data["text"] = text
            st.session_state.data["word_count"] = word_count

    elif st.session_state['active_tab'] == 'URL':
        if url_input and (submit_url or st.session_state.get("url_input_changed", False)):
            text, word_count = load_url(url_input)
            st.session_state.data["text"] = text
            st.session_state.data["word_count"] = word_count
            st.session_state.url_input_changed = False

    elif st.session_state['active_tab'] == 'YouTube':
        if youtube_input and submit_youtube:
            result = process_youtube_input(youtube_input)
            if result:
                st.session_state.data.update(result)

                if len(result['languages']) > 1:
                    st.session_state['show_language_select'] = True 
                    st.experimental_rerun()

                else:
                    transcript_data = load_youtube_transcript(result['video_id'], result['languages'][0])
                    st.session_state.data.update(transcript_data)
        
        # Show language selection dropdown only if needed
        if st.session_state.get('show_language_select', False): 
            selected_language = st.selectbox("Select Language", st.session_state.data['languages'])
            st.session_state.data['selected_language'] = selected_language

            transcript_data = load_youtube_transcript(
                st.session_state.data['video_id'],
                st.session_state.data['selected_language']
            )
            st.session_state.data.update(transcript_data)
            # Remove the flag after language selection
            st.session_state.pop('show_language_select') 

# Tabs for Upload, URL, and YouTube
tab1, tab2, tab3 = st.tabs(["Upload", "URL", "YouTube"])

with tab1:
    st.session_state['active_tab'] = 'Upload'
    display_active_tab()

with tab2:
    st.session_state['active_tab'] = 'URL'
    display_active_tab()

with tab3:
    st.session_state['active_tab'] = 'YouTube'
    display_active_tab()

# Display Extracted Text (if available)
if "text" in st.session_state.data and st.session_state.data["text"]:
    with st.expander(f"Extracted Text (Word count: {st.session_state.data['word_count']}):"):
        st.write(st.session_state.data["text"][:2000])

# Dropdown menu for prompt templates
template_name = st.selectbox("Choose a prompt template", list(prompt_templates.keys()), key="template_name")

# Set the prompt based on the selected template
if st.button("Use Template"):
    st.session_state.settings["prompt"] = prompt_templates[template_name].replace("{text}", "{text}")

# Editable text area for the prompt
prompt = st.text_area("Edit the prompt", value=st.session_state.settings["prompt"], height=300, key="prompt_text_area")

# API call and response handling
if st.button("Generate Summary"):
    prompt_with_text = st.session_state.settings["prompt"].replace("{text}", st.session_state.data["text"])

    with st.spinner("Generating summary..."):
        try:
            if st.session_state.settings["api_provider_index"] == 0:  # OpenAI GPT-4o
                completion = openai_client.chat.completions.create(
                    model=st.session_state.settings["model_name"],
                    messages=[
                        {"role": "user", "content": prompt_with_text}
                    ],
                    temperature=st.session_state.settings["temperature"],
                    max_tokens=st.session_state.settings["max_tokens"]
                )
                st.session_state.data["summary"] = completion.choices[0].message.content
                st.session_state.data["model_used"] = "GPT-4o"

            elif st.session_state.settings["api_provider_index"] == 1:  # Anthropic Claude 3
                message = claude_client.messages.create(
                    model=st.session_state.settings["model_name"],
                    max_tokens=st.session_state.settings["max_tokens"],
                    messages=[
                        {"role": "user", "content": prompt_with_text}
                    ],
                    temperature=st.session_state.settings["temperature"]
                )
                st.session_state.data["summary"] = message.content[0].text
                st.session_state.data["model_used"] = st.session_state.settings["model_name"]

            elif st.session_state.settings["api_provider_index"] == 2:  # Google Gemini
                response = get_gemini_response(
                    st.session_state.settings["model_name"],
                    prompt_with_text,
                    st.session_state.settings["temperature"],
                    st.session_state.settings["max_tokens"]
                )
                st.session_state.data["summary"] = response
                st.session_state.data["model_used"] = st.session_state.settings["model_name"]

        except Exception as e:
            st.session_state.data["summary"] = f"An error occurred during the API call: {str(e)}"
            st.session_state.data["model_used"] = ""

# Create the output area
create_output_area(
    st.session_state.data["summary"] if "summary" in st.session_state.data else "",
    st.session_state.data.get("model_used", "")
)
