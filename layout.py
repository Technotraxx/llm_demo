import streamlit as st
import uuid

from utils import save_text, save_csv, save_doc, save_xls, generate_unique_filename, uploaded_file, url_input, submit_url
from youtube_api import process_youtube_input, load_youtube_transcript
from datetime import datetime

def create_sidebar():
    # Sidebar für Modell-Auswahl und Einstellungen
    st.sidebar.title("Settings")

def create_main_area():
    st.title("Text Summarizer with Multiple LLMs")

    # Tabs for Upload, URL, and YouTube
    tabs = ["Upload", "URL", "YouTube"]
    active_tab = st.tabs(tabs)

    # Function to handle input based on selected tab
    def get_input(tab):
        if tab == "Upload":
            return st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"], key="file_uploader")
        elif tab == "URL":
            url_input = st.text_input("Enter URL", key="url_input")
            submit_url = st.button("Submit URL", key="submit_url")
            return url_input, submit_url
        elif tab == "YouTube":
            youtube_input = st.text_input("Enter YouTube URL or ID", key="youtube_input")
            submit_youtube = st.button("Submit URL or ID", key="submit_youtube")
            return youtube_input, submit_youtube

    # Display content based on active tab
    if active_tab == tabs[0]:
        uploaded_file = get_input(tabs[0])
    elif active_tab == tabs[1]:
        url_input, submit_url = get_input(tabs[1])
    elif active_tab == tabs[2]:
        youtube_input, submit_youtube = get_input(tabs[2])

        # Process YouTube input if submitted
        if youtube_input and submit_youtube:
            result = process_youtube_input(youtube_input)
            if result:
                st.session_state.data.update(result)

                # Handle multiple language scenarios
                if len(result['languages']) > 1:
                    st.session_state['show_language_select'] = True
                    st.rerun()

                else:
                    transcript_data = load_youtube_transcript(result['video_id'], result['languages'][0])
                    st.session_state.data.update(transcript_data)

        # Show language selection dropdown if necessary
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
