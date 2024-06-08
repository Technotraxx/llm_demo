import streamlit as st

def create_main_area():
    st.title("Text Summarizer with Multiple LLMs")

    # Tab labels
    tab_labels = ["Upload", "URL", "YouTube"]
    
    # Initialize active tab in session state if not present
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = tab_labels[0]

    # Get the active tab from session state
    active_tab = st.session_state.active_tab

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

    return uploaded_file, url_input, submit_url, youtube_input, submit_youtube
