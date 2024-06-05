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
    st.experimental_rerun()  # Reload the page to reset the states
