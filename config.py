import streamlit as st
from templates import prompt_templates

def initialize_session_state():
    if "settings" not in st.session_state:
        st.session_state.settings = {
            "api_provider": "Anthropic Claude 3",
            "api_provider_index": 1,
            "model_name": "claude-3-opus-20240229",
            "model_name_index": 0,
            "max_tokens": 512,
            "temperature": 0.7,
            "prompt": prompt_templates["Default Template"]
        }
    if "data" not in st.session_state:
        st.session_state.data = {
            "word_count": 0,
            "summary": "",
            "text": ""
        }
    if "template_name" not in st.session_state:
        st.session_state.template_name = "Default Template"

def reset_session_state():
    st.session_state.settings = {
        "api_provider": "Anthropic Claude 3",
        "api_provider_index": 1,
        "model_name": "claude-3-opus-20240229",
        "model_name_index": 0,
        "max_tokens": 512,
        "temperature": 0.7,
        "prompt": prompt_templates["Default Template"]
    }
    st.session_state.data = {
        "word_count": 0,
        "summary": "",
        "text": ""
    }
    st.session_state.template_name = "Default Template"
    st.rerun()  # Replace st.experimental_rerun with st.rerun

MODEL_OPTIONS = {
    "OpenAI GPT-4o": ["gpt-4o", "gpt-3.5-turbo-16k"],
    "Anthropic Claude 3": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
    "Google Gemini": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro-vision"]
}

def filter_models(api_choice):
    model_options = MODEL_OPTIONS.get(api_choice, [])
    if st.session_state.settings["model_name"] not in model_options:
        st.session_state.settings["model_name"] = model_options[0] if model_options else None
    return model_options

def create_sidebar():
    # Model and API selection
    api_choice_index = st.session_state.settings.get("api_provider_index", 1)
    api_providers = ["OpenAI GPT-4o", "Anthropic Claude 3", "Google Gemini"]
    api_choice = st.sidebar.selectbox(
        "Choose API Provider",
        api_providers,
        index=api_choice_index,
        key="api_provider"
    )
    st.session_state.settings["api_provider_index"] = api_providers.index(api_choice)

    model_options = filter_models(api_choice)
    model_name_index = st.session_state.settings.get("model_name_index", 0)
    if model_name_index >= len(model_options):
        model_name_index = 0
    model_name = st.sidebar.selectbox(
        "Choose Model",
        model_options,
        index=model_name_index,
        key="model_name"
    )
    st.session_state.settings["model_name_index"] = model_options.index(model_name)

    # Einstellungsoptionen
    temperature = st.sidebar.slider(
        "Temperature", 
        min_value=0.0, 
        max_value=1.0, 
        value=st.session_state.settings["temperature"], 
        step=0.1, 
        key="temperature"
    )
    max_tokens = st.sidebar.slider(
        "Max Tokens", 
        min_value=1, 
        max_value=8192 if "gemini" in model_name else 4096, 
        value=st.session_state.settings["max_tokens"], 
        step=1, 
        key="max_tokens"
    )

    # Reset-Button in der Sidebar
    if st.sidebar.button("Reset", key="reset_button"):
        reset_session_state()
