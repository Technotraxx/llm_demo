import streamlit as st
import openai
import anthropic

# Set the API keys
openai_api_key = st.secrets.get("openai_api_key")
claude_api_key = st.secrets.get("anthropic_api_key")

# Initialize the OpenAI client
openai.api_key = openai_api_key

# Initialize the Claude 3 client
claude_client = anthropic.Anthropic(api_key=claude_api_key)

# Auswahl der API
api_choice = st.selectbox("Choose API Provider", ["OpenAI GPT-4o", "Anthropic Claude 3"])

if api_choice == "OpenAI GPT-4o":
    if st.button("Get GPT-4o Response"):
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Help me with my math homework!"},
                {"role": "user", "content": "Hello! Could you solve 2+2?"}
            ]
        )
        st.write("Assistant: " + completion.choices[0].message["content"])

elif api_choice == "Anthropic Claude 3":
    if st.button("Get Claude 3 Response"):
        message = claude_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": "Hello there!"}
            ]
        )
        st.write("Claude 3 Response: " + message['completion'])
