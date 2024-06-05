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

if api_choice == "OpenAI GPT-4o":
    if st.button("Get GPT-4o Response"):
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say this is a test"}
            ]
        )
        st.write("Assistant: " + completion.choices[0].message.content)

elif api_choice == "Anthropic Claude 3":
    if st.button("Get Claude 3 Response"):
        message = claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": "Hello there!"}
            ]
        )
        st.write("Claude 3 Response: " + message.content[0].text)

elif api_choice == "Google Gemini":
    if st.button("Get Google Gemini Response"):
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("The opposite of hot is")
        st.write("Google Gemini Response: " + response.text)
