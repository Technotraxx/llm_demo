import streamlit as st
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

# Set the API keys
openai_api_key = st.secrets.get("openai_api_key")
claude_api_key = st.secrets.get("anthropic_api_key")
google_api_key = st.secrets.get("google_api_key")

# Initialize the OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Initialize the Claude 3 client
claude_client = Anthropic(api_key=claude_api_key)

# Configure Google Gemini
genai.configure(api_key=google_api_key)

# Auswahl der API
api_choice = st.selectbox("Choose API Provider", ["OpenAI GPT-4o", "Anthropic Claude 3", "Google Gemini"])

# Modell-Auswahl und Einstellungen
model_name = ""
if api_choice == "OpenAI GPT-4o":
    model_options = ["gpt-4o", "gpt-3.5-turbo-16k"]
    model_name = st.selectbox("Choose Model", model_options)
elif api_choice == "Anthropic Claude 3":
    model_options = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    model_name = st.selectbox("Choose Model", model_options)
elif api_choice == "Google Gemini":
    model_options = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro", "gemini-pro-vision"]
    model_name = st.selectbox("Choose Model", model_options)

# Temperatur-Slider
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Prompt-Eingabe
prompt = st.text_area("Enter your prompt here", "")

if api_choice == "OpenAI GPT-4o":
    if st.button("Get GPT-4o Response"):
        completion = openai_client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        st.write("Assistant: " + completion.choices[0].message.content)

elif api_choice == "Anthropic Claude 3":
    if st.button("Get Claude 3 Response"):
        message = claude_client.messages.create(
            model=model_name,
            max_tokens=2048,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        st.write("Claude 3 Response: " + message.content[0].text)

elif api_choice == "Google Gemini":
    if st.button("Get Google Gemini Response"):
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt, temperature=temperature)
        st.write("Google Gemini Response: " + response.text)
