import streamlit as st
from api_helpers import (
    openai_models, claude_models, gemini_models,
    get_openai_response, get_claude_response, get_gemini_response
)
from templates import prompt_templates
from utils import save_text, save_csv, save_doc, save_xls, send_email, reload_page, generate_unique_filename
from layout import create_sidebar, create_main_area, create_output_area

# Create the sidebar
create_sidebar()

# API-Auswahl und Modell-Auswahl in der Sidebar
api_choice = st.sidebar.selectbox("Choose API Provider", ["OpenAI GPT-4o", "Anthropic Claude 3", "Google Gemini"])
model_name = ""
if api_choice == "OpenAI GPT-4o":
    model_name = st.sidebar.selectbox("Choose Model", openai_models)
    max_tokens = st.sidebar.slider("Max Tokens", min_value=1, max_value=4096, value=2048, step=1)
elif api_choice == "Anthropic Claude 3":
    model_name = st.sidebar.selectbox("Choose Model", claude_models)
    max_tokens = st.sidebar.slider("Max Tokens", min_value=1, max_value=4096, value=2048, step=1)
elif api_choice == "Google Gemini":
    model_name = st.sidebar.selectbox("Choose Model", gemini_models)
    max_tokens = st.sidebar.slider("Max Tokens", min_value=1, max_value=8192, value=2048, step=1)

# Temperatur-Slider in der Sidebar
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Reset-Button in der Sidebar
if st.sidebar.button("Reset"):
    reload_page()

# Create the main area
uploaded_file = create_main_area()

# Prompt-Eingabe
prompt = st.text_area("Enter your prompt here", "")

# Prompt-Generierung und Ausgabe
if api_choice == "OpenAI GPT-4o":
    if st.button("Get GPT-4o Response"):
        response = get_openai_response(model_name, prompt, temperature, max_tokens)
        create_output_area(response)

elif api_choice == "Anthropic Claude 3":
    if st.button("Get Claude 3 Response"):
        response = get_claude_response(model_name, prompt, temperature, max_tokens)
        create_output_area(response)

elif api_choice == "Google Gemini":
    if st.button("Get Google Gemini Response"):
        response = get_gemini_response(model_name, prompt, temperature, max_tokens)
        create_output_area(response)
