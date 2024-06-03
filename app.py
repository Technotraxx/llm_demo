```python
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
    MODEL_NAME = "claude-3-opus-20240229"

    def get_completion(client, prompt):
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=[{
                "role": 'user', "content":  prompt
            }]
        )
        return response['content']

    if st.button("Generate Summary"):
        completion = get_completion(client,
            f"""Here is an academic paper: <paper>{text}</paper>

            Please do the following:
            1. Summarize the abstract at a kindergarten reading level. (In <kindergarten_abstract> tags.)
            2. Write the Methods section as a recipe from the Moosewood Cookbook. (In <moosewood_methods> tags.)
            3. Compose a short poem epistolizing the results in the style of Homer. (In <homer_results> tags.)
            """
        )
        st.write("Summary:")
        st.write(completion)
```
