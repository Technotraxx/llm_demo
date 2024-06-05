import streamlit as st
from apis.anthropic_claude import AnthropicClaudeAPI, get_model_settings as get_claude_settings
from apis.google_gemini import GoogleGeminiAPI, get_model_settings as get_gemini_settings
from apis.openai_gpt import OpenAIGPT4oAPI, get_model_settings as get_gpt_settings

# Set the API keys
openai_api_key = st.secrets.get("openai_api_key")
claude_api_key = st.secrets.get("anthropic_api_key")
google_api_key = st.secrets.get("google_api_key")

# Auswahl der API
api_choice = st.selectbox("Choose API Provider", ["OpenAI GPT-4o", "Anthropic Claude 3", "Google Gemini"])

# Modell-Auswahl und Einstellungen
if api_choice == "OpenAI GPT-4o":
    model_options = ["gpt-4o", "gpt-3.5-turbo-16k"]
    model_name = st.selectbox("Choose Model", model_options)
    settings = get_gpt_settings(model_name)

elif api_choice == "Anthropic Claude 3":
    model_options = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    model_name = st.selectbox("Choose Model", model_options)
    settings = get_claude_settings(model_name)

elif api_choice == "Google Gemini":
    model_options = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro-vision"]
    model_name = st.selectbox("Choose Model", model_options)
    settings = get_gemini_settings(model_name)

# Einstellungsoptionen
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=settings["default_temperature"])
max_tokens = st.slider("Max Tokens", min_value=1, max_value=settings["max_output_tokens"], value=settings["default_max_tokens"])
top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=settings.get("default_top_p", 1.0))
frequency_penalty = st.slider("Frequency Penalty", min_value=0.0, max_value=2.0, value=settings.get("default_frequency_penalty", 0.0))
presence_penalty = st.slider("Presence Penalty", min_value=0.0, max_value=2.0, value=settings.get("default_presence_penalty", 0.0))

# Prompt-Eingabe
prompt = st.text_area("Enter your prompt here", "")

# API Client Initialisierung
if api_choice == "OpenAI GPT-4o":
    api_client = OpenAIGPT4oAPI(api_key=openai_api_key, model_name=model_name)
elif api_choice == "Anthropic Claude 3":
    api_client = AnthropicClaudeAPI(api_key=claude_api_key, model_name=model_name)
elif api_choice == "Google Gemini":
    api_client = GoogleGeminiAPI(api_key=google_api_key, model_name=model_name)

# API-Aufruf und Ausgabe
if st.button("Generate Response"):
    if api_choice == "OpenAI GPT-4o":
        messages = [{"role": "user", "content": prompt}]
        response = api_client.generate_completion(messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty)
        st.write("Response: " + response.choices[0].message.content)

    elif api_choice == "Anthropic Claude 3":
        response = api_client.generate_completion(prompt, max_tokens, temperature)
        st.write("Response: " + response.content[0].text)

    elif api_choice == "Google Gemini":
        response = api_client.generate_content(prompt, temperature, top_p, max_tokens)
        st.write("Response: " + response.text)
