import streamlit as st
from pypdf import PdfReader
from anthropic import Anthropic

# PDF Upload
st.title("PDF Text Summarizer with Claude 3 LLM")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    number_of_pages = len(reader.pages)
    text = ''.join(page.extract_text() for page in reader.pages)
    
    st.write("Extracted Text:")
    st.write(text[:2000])  # Display the first 2000 characters

    # Holen Sie den API-Schlüssel aus den Streamlit Secrets
    api_key = st.secrets["anthropic_api_key"]

    client = Anthropic(api_key=api_key)
    
    # Dropdown menu to choose the model
    model_options = {
        "Claude 3 Opus": "claude-3-opus-20240229",
        "Claude 3 Sonnet": "claude-3-sonnet-20240229",
        "Claude 3 Haiku": "claude-3-haiku-20240307"
    }
    model_name = st.selectbox("Choose a model", list(model_options.keys()))

    # Slider for max_tokens
    max_tokens = st.slider("Max Tokens", min_value=0, max_value=4096, value=256, step=256)

    # Slider for temperature
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.9, step=0.1)

    # Default prompt text
    default_prompt = f"""Here is an academic paper: <paper>{text}</paper>

            Please do the following:
            1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)
            2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)
            3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)
            """
    
    # Editable text area for the prompt
    prompt = st.text_area("Edit the prompt", default_prompt, height=300)

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
