import streamlit as st
from pypdf import PdfReader
from anthropic import Anthropic
from templates import prompt_templates
from utils import save_text, save_csv, save_doc, save_xls, send_email
from layout import create_sidebar, create_main_area, create_output_area

# Initialize session state variables
if "model_name" not in st.session_state:
    st.session_state.model_name = "Claude 3 Opus"
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 256
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.9
if "prompt" not in st.session_state:
    st.session_state.prompt = prompt_templates["Default Template"]
if "word_count" not in st.session_state:
    st.session_state.word_count = 0
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Create sidebar
create_sidebar()

# Create main area
uploaded_file = create_main_area()

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    number_of_pages = len(reader.pages)
    text = ''.join(page.extract_text() for page in reader.pages)
    word_count = len(text.split())
    st.session_state.word_count = word_count

    st.write("Extracted Text:")
    st.write(text[:2000])  # Display the first 2000 characters
    st.write(f"Word count: {word_count}")

    api_key = st.secrets["anthropic_api_key"]
    client = Anthropic(api_key=api_key)

    model_options = {
        "Claude 3 Opus": "claude-3-opus-20240229",
        "Claude 3 Sonnet": "claude-3-sonnet-20240229",
        "Claude 3 Haiku": "claude-3-haiku-20240307"
    }
    model_name = st.session_state.model_name
    max_tokens = st.session_state.max_tokens
    temperature = st.session_state.temperature

    # Dropdown menu for prompt templates
    template_name = st.selectbox("Choose a prompt template", list(prompt_templates.keys()))

    # Set the prompt based on the selected template
    if st.button("Use Template"):
        st.session_state.prompt = prompt_templates[template_name].replace("{text}", "{text}")

    # Editable text area for the prompt
    prompt = st.text_area("Edit the prompt", key="prompt", value=st.session_state.prompt, height=300)

    def get_completion(client, prompt, model_name, max_tokens, temperature):
        try:
            response = client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{
                    "role": 'user', "content":  prompt
                }]
            )
            return response.content[0].text
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return ""

    if st.button("Generate Summary"):
        # Replacing {text} in the user-edited prompt
        prompt_with_text = prompt.replace("{text}", text)
        completion = get_completion(client,
            prompt_with_text, model_options[model_name], max_tokens, temperature
        )
        if completion:
            st.session_state.summary = completion

# Create output area
create_output_area(st.session_state.summary)
