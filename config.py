import streamlit as st
from templates import prompt_templates

def initialize_session_state():
    if "settings" not in st.session_state:
        st.session_state.settings = {
            "api_provider": "Anthropic Claude 3",
            "model_name": "claude-3-opus-20240229",
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
        "model_name": "claude-3-opus-20240229",
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
    st.session_state.api_provider = "Anthropic Claude 3"
    st.session_state.model_name = "claude-3-opus-20240229"
    st.experimental_rerun()  # Reload the page to reset the states


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
