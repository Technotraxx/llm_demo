import streamlit as st
from pypdf import PdfReader
from anthropic_claude3 import AnthropicClaude3API
from openai_gpt4o import OpenAIGPT4oAPI
from config_anthropic_claude3 import DEFAULT_MODEL_NAME as CLAUDE_MODEL
from config_openai_gpt4o import DEFAULT_MODEL_NAME as GPT4O_MODEL
from templates import prompt_templates
from utils import save_text, save_csv, save_doc, save_xls, send_email, reload_page, generate_unique_filename
from layout import create_sidebar, create_main_area, create_output_area

# Initialize session state variables
if "api_provider" not in st.session_state:
    st.session_state.api_provider = "Anthropic Claude 3"
if "model_name" not in st.session_state:
    st.session_state.model_name = CLAUDE_MODEL if st.session_state.api_provider == "Anthropic Claude 3" else GPT4O_MODEL
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2048 if st.session_state.api_provider == "Anthropic Claude 3" else 1500
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.9 if st.session_state.api_provider == "Anthropic Claude 3" else 0.5
if "prompt" not in st.session_state:
    st.session_state.prompt = prompt_templates["Default Template"]
if "word_count" not in st.session_state:
    st.session_state.word_count = 0
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "text" not in st.session_state:
    st.session_state.text = ""

# Create sidebar
create_sidebar()

# Create main area
uploaded_file = create_main_area()

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    number_of_pages = len(reader.pages)
    text = ''.join(page.extract_text() for page in reader.pages)
    word_count = len(text.split())
    st.session_state.word_count = word_count
    st.session_state.text = text

if "text" in st.session_state and st.session_state.text:
    with st.expander(f"Extracted Text (Word count: {st.session_state.word_count}):"):
        st.write(st.session_state.text[:2000])  # Display the first 2000 characters

api_provider = st.selectbox("Choose API Provider", ["Anthropic Claude 3", "OpenAI GPT-4o"], key="api_provider")

if api_provider == "Anthropic Claude 3":
    api_key = st.secrets["anthropic_api_key"]
    api_client = AnthropicClaude3API(api_key=api_key, model_name=st.session_state.model_name)
elif api_provider == "OpenAI GPT-4o":
    api_key = st.secrets["openai_api_key"]
    api_client = OpenAIGPT4oAPI(api_key=api_key, model_name=st.session_state.model_name)

# Editable text area for the prompt
prompt = st.text_area("Edit the prompt", value=st.session_state.prompt, height=300, key="prompt_text_area")

def get_completion(messages, model_name, max_tokens, temperature, top_p, frequency_penalty, presence_penalty):
    if st.session_state.api_provider == "Anthropic Claude 3":
        response = api_client.generate_completion(
            prompt=messages,
            max_tokens=max_tokens
        )
        return response.messages[0].text
    elif st.session_state.api_provider == "OpenAI GPT-4o":
        response = api_client.generate_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        return response.choices[0].message["content"]

if st.button("Generate Summary"):
    st.session_state.prompt = st.session_state.prompt_text_area
    prompt_with_text = st.session_state.prompt.replace("{text}", st.session_state.text)
    messages = [
        {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
        {"role": "user", "content": [{"type": "text", "text": prompt_with_text}]}
    ]
    completion = get_completion(
        messages=prompt_with_text if st.session_state.api_provider == "Anthropic Claude 3" else messages,
        model_name=st.session_state.model_name,
        max_tokens=st.session_state.max_tokens,
        temperature=st.session_state.temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    st.session_state.summary = completion

# Create output area
create_output_area(st.session_state.summary)
