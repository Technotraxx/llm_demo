import os
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
import streamlit as st

def initialize_clients():
    openai_api_key = st.secrets["openai"]["api_key"]
    claude_api_key = st.secrets["anthropic"]["api_key"]
    google_api_key = st.secrets["google"]["api_key"]

    openai_client = OpenAI(api_key=openai_api_key)
    claude_client = Anthropic(api_key=claude_api_key)
    genai.configure(api_key=google_api_key)

    return openai_client, claude_client, genai

# Function to generate response
def get_openai_response(openai_client, model_name, prompt, temperature, max_tokens):
    completion = openai_client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return completion.choices[0].message.content

def get_claude_response(claude_client, model_name, prompt, temperature, max_tokens):
    message = claude_client.messages.create(
        model=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def get_gemini_response(model_name, prompt, temperature, max_tokens):
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings=safety_settings,
            generation_config=generation_config,
        )
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        
        if response.text:
            return response.text
        else:
            return "No output from Gemini."

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

def generate_summary(openai_client, claude_client, model_name, prompt, temperature, max_tokens, api_provider_index):
    st.write(f"Generating summary with model: {model_name} and provider index: {api_provider_index}")
    if api_provider_index == 0:  # OpenAI
        return get_openai_response(openai_client, model_name, prompt, temperature, max_tokens), model_name
    elif api_provider_index == 1:  # Anthropic Claude 3
        return get_claude_response(claude_client, model_name, prompt, temperature, max_tokens), model_name
    elif api_provider_index == 2:  # Google Gemini
        return get_gemini_response(model_name, prompt, temperature, max_tokens), model_name
    else:
        raise ValueError("Invalid API provider index")


