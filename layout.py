import streamlit as st
import uuid

from utils import save_text, save_csv, save_doc, save_xls, generate_unique_filename, extract_video_id, list_available_transcripts
from datetime import datetime

def create_sidebar():
    # Sidebar für Modell-Auswahl und Einstellungen
    st.sidebar.title("Settings")

def create_main_area():
    st.title("Text Summarizer with Multiple LLMs")

    # Tabs für Upload und URL
    tab1, tab2, tab3 = st.tabs(["Upload", "URL", "YouTube"])

    uploaded_file = None
    url_input = None
    youtube_input = None
    languages = None
    selected_language = None
    submit_youtube = None

    with tab1:
        uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"], key="file_uploader")

    with tab2:
        url_input = st.text_input("Enter URL", key="url_input")
        submit_url = st.button("Submit URL", key="submit_url")

    with tab3:
        youtube_input = st.text_input("Enter YouTube URL or ID", key="youtube_input")
        submit_youtube = st.button("Submit URL or ID", key="submit_youtube")

        if youtube_input:
            video_id = extract_video_id(youtube_input)
            if video_id:
                languages = list_available_transcripts(video_id)
                if languages:
                    unique_key = f"language_select_{video_id}_{uuid.uuid4()}"
                    selected_language = st.selectbox("Select Language", languages, key=unique_key)
                    st.session_state.selected_language = selected_language

    return uploaded_file, url_input, submit_url, youtube_input, submit_youtube, selected_language

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
