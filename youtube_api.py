import re
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable, TranscriptsDisabled, NoTranscriptFound
import streamlit as st

def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|)([a-zA-Z0-9_-]{11})'
    match = re.match(pattern, url)
    return match.group(1) if match else None

def load_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([t['text'] for t in transcript_list])
        word_count = len(transcript.split())
        return transcript, word_count
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        st.error(f"Error loading transcript: {str(e)}")
        return None, 0

def process_youtube_input(youtube_input):
    video_id = extract_video_id(youtube_input)
    if not video_id:
        st.error("Invalid YouTube URL or ID.")
        return None
    text, word_count = load_youtube_transcript(video_id)
    if text:
        return {"text": text, "word_count": word_count, "video_id": video_id, "languages": ["en"], "selected_language": "en"}
    else:
        return None

def handle_youtube_input(youtube_input):
    result = process_youtube_input(youtube_input)
    if result:
        st.session_state.data.update(result)
    else:
        st.warning("Failed to process YouTube input.")

# Deaktivieren der Sprach-Auswahlfunktion
# def handle_language_selection():
#     if st.session_state.get('show_language_select', False):
#         st.write("Select Transcript Language:")
#         selected_language = st.selectbox("Select Language", st.session_state.data['languages'], key='selected_language_selectbox')
        
#         # Debugging: Überprüfen der Auswahl der Sprache
#         st.write(f"Selected Language: {selected_language}")
        
#         text_data = load_youtube_transcript(st.session_state.data['video_id'], selected_language)
        
#         # Debugging: Überprüfen der geladenen Transkript-Daten
#         st.write(f"Loaded Transcript Data: {text_data}")
        
#         st.session_state.data.update({'text': text_data['text'], 'word_count': text_data['word_count'], 'selected_language': selected_language})
#         st.session_state.show_language_select = False
#         st.session_state.active_tab = "YouTube"  # Sicherstellen, dass der aktive Tab korrekt gesetzt wird
