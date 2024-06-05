import streamlit as st
from api_helpers import (
    openai_models, claude_models, gemini_models,
    get_openai_response, get_claude_response, get_gemini_response
)

# Auswahl der API
api_choice = st.selectbox("Choose API Provider", ["OpenAI GPT-4o", "Anthropic Claude 3", "Google Gemini"])

# Modell-Auswahl und Einstellungen
model_name = ""
max_tokens = 2048
if api_choice == "OpenAI GPT-4o":
    model_name = st.selectbox("Choose Model", openai_models)
    max_tokens = st.slider("Max Tokens", min_value=1, max_value=4096, value=2048, step=1)
elif api_choice == "Anthropic Claude 3":
    model_name = st.selectbox("Choose Model", claude_models)
    max_tokens = st.slider("Max Tokens", min_value=1, max_value=4096, value=2048, step=1)
elif api_choice == "Google Gemini":
    model_name = st.selectbox("Choose Model", gemini_models)
    max_tokens = st.slider("Max Tokens", min_value=1, max_value=8192, value=2048, step=1)

# Temperatur-Slider
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Prompt-Eingabe
prompt = st.text_area("Enter your prompt here", "")

if api_choice == "OpenAI GPT-4o":
    if st.button("Get GPT-4o Response"):
        response = get_openai_response(model_name, prompt, temperature, max_tokens)
        st.write("Assistant: " + response)

elif api_choice == "Anthropic Claude 3":
    if st.button("Get Claude 3 Response"):
        response = get_claude_response(model_name, prompt, temperature, max_tokens)
        st.write("Claude 3 Response: " + response)

elif api_choice == "Google Gemini":
    if st.button("Get Google Gemini Response"):
        response = get_gemini_response(model_name, prompt, temperature, max_tokens)
        st.write("Google Gemini Response: " + response)
