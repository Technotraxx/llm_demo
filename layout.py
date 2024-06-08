import streamlit as st
import uuid
from datetime import datetime

from utils import (save_file, send_email, reload_page, generate_unique_filename, load_pdf, load_docx,
                   load_txt, load_csv, load_url)
from youtube_api import process_youtube_input

def create_sidebar():
    st.sidebar.title("Settings")

def create_main_area():
    st.title("Text Summarizer with Multiple LLMs")

    # Tab labels
    tab_labels = ["Upload", "URL", "YouTube"]
    
    # Initialize active tab in session state if not present
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = tab_labels[0]

    # Get the active tab from session state
    active_tab = st.session_state.active_tab

    # Debugging: Anzeige des aktuellen Tabs
    st.write(f"Active Tab: {active_tab}")

    # Create tabs and determine the active tab
    tab1, tab2, tab3 = st.tabs(tab_labels)
    uploaded_file, url_input, submit_url, youtube_input, submit_youtube = None, None, None, None, None

    with tab1:
        uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"], key="file_uploader")
        if active_tab == "Upload":
            st.session_state.active_tab = "Upload"

    with tab2:
        url_input = st.text_input("Enter URL", key="url_input")
        submit_url = st.button("Submit URL", key="submit_url")
        if active_tab == "URL":
            st.session_state.active_tab = "URL"

    with tab3:
        youtube_input = st.text_input("Enter YouTube URL or ID", key="youtube_input")
        submit_youtube = st.button("Submit URL or ID", key="submit_youtube")
        if active_tab == "YouTube":
            st.session_state.active_tab = "YouTube"

    # Update the active tab in session state based on user interaction
    if submit_url:
        st.session_state.active_tab = "URL"
    if submit_youtube:
        st.session_state.active_tab = "YouTube"

    # Debugging: Anzeige des aktualisierten Tabs
    st.write(f"Updated Active Tab: {st.session_state.active_tab}")

    return uploaded_file, url_input, submit_url, youtube_input, submit_youtube

def handle_uploaded_file(uploaded_file):
    if uploaded_file:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == 'pdf':
            text, word_count = load_pdf(uploaded_file)
        elif file_type == 'docx':
            text, word_count = load_docx(uploaded_file)
        elif file_type == 'txt':
            text, word_count = load_txt(uploaded_file)
        elif file_type == 'csv':
            text, word_count = load_csv(uploaded_file)

        st.session_state.data["text"] = text
        st.session_state.data["word_count"] = word_count

def handle_url_input(url_input, submit_url):
    if url_input:
        st.session_state.url_input_changed = True

    if url_input and (submit_url or st.session_state.get("url_input_changed", False)):
        text, word_count = load_url(url_input)
        st.session_state.data["text"] = text
        st.session_state.data["word_count"] = word_count
        st.session_state.url_input_changed = False

def handle_template_selection(prompt_templates):
    template_name = st.selectbox("Choose a prompt template", list(prompt_templates.keys()), key="template_name")

    if st.button("Use Template"):
        st.session_state.settings["prompt"] = prompt_templates[template_name].replace("{text}", "{text}")

    prompt = st.text_area("Edit the prompt", value=st.session_state.settings["prompt"], height=300, key="prompt_text_area")

    return prompt

def create_output_area(summary, model_name):
    if summary:
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        st.header("Output:")
        st.markdown(f"**Created with {model_name}** am _{now}_.")

        st.markdown(summary)
        st.divider()

        with st.expander("Copy to Clipboard"):
            st.code(summary, language='markdown', line_numbers=True)

        with st.expander("Save and Send Options"):
            st.write("Save the summary:")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Save as TXT", key="save_txt_button"):
                    filename = generate_unique_filename("summary", "txt")
                    save_file(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download TXT", data=file, file_name=filename, mime="text/plain")
            with col2:
                if st.button("Save as CSV", key="save_csv_button"):
                    filename = generate_unique_filename("summary", "csv")
                    save_file(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download CSV", data=file, file_name=filename, mime="text/csv")
            with col3:
                if st.button("Save as DOC", key="save_doc_button"):
                    filename = generate_unique_filename("summary", "docx")
                    save_file(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download DOC", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            with col4:
                if st.button("Save as XLS", key="save_xls_button"):
                    filename = generate_unique_filename("summary", "xlsx")
                    save_file(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download XLS", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            st.write("Send the summary via email:")
            email_address = st.text_input("Email address", key="email_address")
            if st.button("Send Email", key="send_email_button"):
                send_email("Summary from Multiple LLMs", summary, email_address, st.secrets["email"], st.secrets["email_password"])
