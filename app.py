import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from templates import prompt_templates
from utils import save_text, save_csv, save_doc, save_xls, send_email, reload_page, generate_unique_filename
from layout import create_sidebar, create_main_area, create_output_area
from config import initialize_session_state, filter_models, reset_session_state

# Set API keys
openai_api_key = st.secrets.get("openai_api_key")
claude_api_key = st.secrets.get("anthropic_api_key")
google_api_key = st.secrets.get("google_api_key")

# Initialize the clients
openai_client = OpenAI(api_key=openai_api_key)
claude_client = Anthropic(api_key=claude_api_key)
genai.configure(api_key=google_api_key)

# Initialize session state variables
initialize_session_state(st)

# Sidebar settings
create_sidebar()

# Model and API selection
api_choice = st.sidebar.selectbox("Choose API Provider", ["OpenAI GPT-4o", "Anthropic Claude 3", "Google Gemini"], key="api_provider")
model_options = filter_models(api_choice)
model_name = st.sidebar.selectbox("Choose Model", model_options, key="model_name")

# Einstellungsoptionen
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.settings["temperature"], step=0.1, key="temperature")
max_tokens = st.sidebar.slider("Max Tokens", min_value=1, max_value=8192 if "gemini" in model_name else 4096, value=st.session_state.settings["max_tokens"], step=1, key="max_tokens")

# Reset-Button in der Sidebar
if st.sidebar.button("Reset"):
    reset_session_state(st)

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

    if api_choice == "OpenAI GPT-4o":
        completion = openai_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt_with_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        st.session_state.data["summary"] = completion.choices[0].message.content

    elif api_choice == "Anthropic Claude 3":
        message = claude_client.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": prompt_with_text}
            ],
            temperature=temperature
        )
        st.session_state.data["summary"] = message.content[0].text

    elif api_choice == "Google Gemini":
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        response = model.generate_content(prompt_with_text)
        if response.candidates:
            st.session_state.data["summary"] = response.candidates[0].text
        else:
            st.session_state.data["summary"] = "No response received. Please check the `response.prompt_feedback` for details."
            st.write(response.prompt_feedback)

# Create the output area
create_output_area(st.session_state.data["summary"] if "summary" in st.session_state.data else "")
