import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from templates import prompt_templates
from utils import save_text, save_csv, save_doc, save_xls, send_email, reload_page, generate_unique_filename
from layout import create_sidebar as create_layout_sidebar, create_main_area, create_output_area
from config import initialize_session_state, create_sidebar
from api_helpers import get_gemini_response 

# Set API keys
openai_api_key = st.secrets.get("openai_api_key")
claude_api_key = st.secrets.get("anthropic_api_key")
google_api_key = st.secrets.get("google_api_key")

# Initialize the clients
openai_client = OpenAI(api_key=openai_api_key)
claude_client = Anthropic(api_key=claude_api_key)
genai.configure(api_key=google_api_key)

# Initialize session state variables
initialize_session_state()

# Sidebar settings
create_sidebar()

# Create main area
uploaded_file = create_main_area()

@st.cache_data
def load_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ''.join(page.extract_text() for page in reader.pages)
    word_count = len(text.split())
    return text, word_count

if uploaded_file:
    text, word_count = load_pdf(uploaded_file)
    st.session_state.data["text"] = text
    st.session_state.data["word_count"] = word_count

if "text" in st.session_state.data and st.session_state.data["text"]:
    with st.expander(f"Extracted Text (Word count: {st.session_state.data['word_count']}):"):
        st.write(st.session_state.data["text"][:2000])  # Display the first 2000 characters

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

        elif st.session_state.settings["api_provider_index"] == 2:  # Google Gemini
            response = get_gemini_response(
                st.session_state.settings["model_name"],
                prompt_with_text,
                st.session_state.settings["temperature"],
                st.session_state.settings["max_tokens"]
            )
            st.session_state.data["summary"] = response
            st.subheader("Gemini:")
            st.write(response)

    except Exception as e:
        st.write(f"An error occurred during the API call: {str(e)}")

# Create the output area
create_output_area(st.session_state.data["summary"] if "summary" in st.session_state.data else "")
