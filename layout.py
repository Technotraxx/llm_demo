import streamlit as st
import uuid

from utils import save_text, save_csv, save_doc, save_xls, generate_unique_filename
from datetime import datetime

def create_sidebar():
    # Sidebar für Modell-Auswahl und Einstellungen
    st.sidebar.title("Settings")

import streamlit as st
from youtube_api import process_youtube_input, load_youtube_transcript

def create_main_area():
    st.title("Text Summarizer with Multiple LLMs")

    # Tabs for Upload, URL, and YouTube
    tab1, tab2, tab3 = st.tabs(["Upload", "URL", "YouTube"])

    # Initialize active_tab in session state if not present
    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = 'Upload'

    # Function to simulate tab switching and handle input
    def display_tab_content(tab):
        if tab == 'Upload':
            uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"], key="file_uploader")
            return uploaded_file
        elif tab == 'URL':
            url_input = st.text_input("Enter URL", key="url_input")
            submit_url = st.button("Submit URL", key="submit_url")
            return url_input, submit_url
        elif tab == 'YouTube':
            youtube_input = st.text_input("Enter YouTube URL or ID", key="youtube_input")
            submit_youtube = st.button("Submit URL or ID", key="submit_youtube")
            return youtube_input, submit_youtube

    # Display content based on active tab
    with tab1:
        st.session_state['active_tab'] = 'Upload'
        uploaded_file = display_tab_content('Upload')

    with tab2:
        st.session_state['active_tab'] = 'URL'
        url_input, submit_url = display_tab_content('URL')

    with tab3:
        st.session_state['active_tab'] = 'YouTube'
        youtube_input, submit_youtube = display_tab_content('YouTube')

        if youtube_input and submit_youtube:
            result = process_youtube_input(youtube_input)
            if result:
                st.session_state.data.update(result)

                if len(result['languages']) > 1:
                    st.session_state['show_language_select'] = True
                    st.experimental_rerun()

                else:
                    transcript_data = load_youtube_transcript(result['video_id'], result['languages'][0])
                    st.session_state.data.update(transcript_data)

        # Show language selection dropdown only if needed
        if st.session_state.get('show_language_select', False):
            selected_language = st.selectbox("Select Language", st.session_state.data['languages'])
            st.session_state.data['selected_language'] = selected_language

            transcript_data = load_youtube_transcript(
                st.session_state.data['video_id'],
                st.session_state.data['selected_language']
            )
            st.session_state.data.update(transcript_data)
            # Remove the flag after language selection
            st.session_state.pop('show_language_select')

    return uploaded_file, url_input, submit_url, youtube_input, submit_youtube

def create_output_area(summary, model_name):
    if summary:
        # Aktuelles Datum und Uhrzeit in deutscher Schreibweise
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        st.header("Output:")
        st.markdown(f"**Created with {model_name}** am _{now}_.")

        st.markdown(summary)
        st.divider()

        # Display the summary using markdown
        with st.expander("Copy to Clipboard"):
            st.code(summary, language='markdown', line_numbers=True)

        with st.expander("Save and Send Options"):
            # Save options
            st.write("Save the summary:")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("Save as TXT", key="save_txt_button"):
                    filename = generate_unique_filename("summary", "txt")
                    save_text(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download TXT", data=file, file_name=filename, mime="text/plain")
            with col2:
                if st.button("Save as CSV", key="save_csv_button"):
                    filename = generate_unique_filename("summary", "csv")
                    save_csv(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "r") as file:
                        st.download_button(label="Download CSV", data=file, file_name=filename, mime="text/csv")
            with col3:
                if st.button("Save as DOC", key="save_doc_button"):
                    filename = generate_unique_filename("summary", "docx")
                    save_doc(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download DOC", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            with col4:
                if st.button("Save as XLS", key="save_xls_button"):
                    filename = generate_unique_filename("summary", "xlsx")
                    save_xls(filename, summary)
                    st.success(f"Saved as {filename}")
                    with open(filename, "rb") as file:
                        st.download_button(label="Download XLS", data=file, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            # Email option
            st.write("Send the summary via email:")
            email_address = st.text_input("Email address", key="email_address")
            if st.button("Send Email", key="send_email_button"):
                send_email("Summary from Multiple LLMs", summary, email_address, st.secrets["email"], st.secrets["email_password"])
