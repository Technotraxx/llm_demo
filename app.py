import streamlit as st
from pypdf import PdfReader
from anthropic import Anthropic

# Function to reset session state
def reset_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Initialize session state variables
if "model_name" not in st.session_state:
    st.session_state.model_name = "Claude 3 Opus"
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2048
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.9
if "prompt" not in st.session_state:
    st.session_state.prompt = """Here is an academic paper: <paper>{text}</paper>

    Please do the following:
    1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)
    2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)
    3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)
    """
if "word_count" not in st.session_state:
    st.session_state.word_count = 0

# Title
st.title("PDF Text Summarizer with Claude 3 LLM")

# Reset button
if st.button("Reset"):
    reset_session_state()

# PDF Upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    number_of_pages = len(reader.pages)
    text = ''.join(page.extract_text() for page in reader.pages)
    word_count = len(text.split())
    st.session_state.word_count = word_count

    st.write("Extracted Text:")
    st.write(text[:2000])  # Display the first 2000 characters
    st.write(f"Word count: {word_count}")

    # Holen Sie den API-Schlüssel aus den Streamlit Secrets
    api_key = st.secrets["anthropic_api_key"]

    client = Anthropic(api_key=api_key)

    # Dropdown menu to choose the model
    model_options = {
        "Claude 3 Opus": "claude-3-opus-20240229",
        "Claude 3 Sonnet": "claude-3-sonnet-20240229",
        "Claude 3 Haiku": "claude-3-haiku-20240307"  # Verify the identifier
    }
    model_name = st.selectbox("Choose a model", list(model_options.keys()), key="model_name")

    # Slider for max_tokens
    max_tokens = st.slider("Max Tokens", min_value=0, max_value=4096, value=st.session_state.max_tokens, step=256, key="max_tokens")

    # Slider for temperature
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.1, key="temperature")

    # Prompt templates
    prompt_templates = {
        "Template A": "Prompt text for template A",
        "Template B": "Prompt text for template B",
        "Template C": "Prompt text for template C",
        "Template D": "Prompt text for template D",
        "Template E": "Prompt text for template E"
    }
    template_name = st.selectbox("Choose a prompt template", list(prompt_templates.keys()))

    # Set the prompt based on the selected template
    if st.button("Use Template"):
        st.session_state.prompt = prompt_templates[template_name].replace("{text}", "{text}")

    # Editable text area for the prompt
    prompt = st.text_area("Edit the prompt", st.session_state.prompt, height=300, key="prompt")

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
            st.write("Summary:")
            st.write(completion)

else:
    st.write("Word count: 0")
