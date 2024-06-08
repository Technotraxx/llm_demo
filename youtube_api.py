import re
import uuid
from youtube_transcript_api import (YouTubeTranscriptApi, VideoUnavailable,
                                   TranscriptsDisabled, NoTranscriptFound)
import streamlit as st

def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|)([a-zA-Z0-9_-]{11})'
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return None

def list_available_transcripts(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = [transcript.language_code for transcript in transcript_list]
        return languages
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        st.error(f"Error: {str(e)}")
        return []

def load_youtube_transcript(video_id, selected_language):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language])
        transcript = ' '.join([t['text'] for t in transcript_list])
        word_count = len(transcript.split())
        return {
            "text": transcript,
            "word_count": word_count
        }
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        st.error(f"Error: {str(e)}")
        return {"error": str(e), "success": False}

def process_youtube_input(youtube_input):
    video_id = extract_video_id(youtube_input)
    if not video_id:
        return None

    languages = list_available_transcripts(video_id)
    if not languages:
        return None
    
    unique_key = f"language_select_{uuid.uuid4()}"
    selected_language = st.selectbox("Select Language", languages, key=unique_key)

    if selected_language:
        transcript_data = load_youtube_transcript(video_id, selected_language)
        if "error" in transcript_data:
            return None
        else:
            return {
                "video_id": video_id,
                "languages": languages,
                "selected_language": selected_language,
                "text": transcript_data["text"],
                "word_count": transcript_data["word_count"]
            }

def handle_youtube_input(youtube_input):
    result = process_youtube_input(youtube_input)
    if result:
        st.session_state.data.update(result)
        if len(result['languages']) > 1:
            st.session_state.show_language_select = True
        else:
            text_data = load_youtube_transcript(result['video_id'], result['languages'][0])
            st.session_state.data.update({'text': text_data['text'], 'word_count': text_data['word_count']})
    else:
        st.warning("Failed to process YouTube input.")

def handle_language_selection():
    if st.session_state.get('show_language_select', False):
        st.write("Select Transcript Language:")
        selected_language = st.selectbox("Select Language", st.session_state.data['languages'])
        
        # Debugging: Überprüfen der Auswahl der Sprache
        st.write(f"Selected Language: {selected_language}")
        
        text_data = load_youtube_transcript(st.session_state.data['video_id'], selected_language)
        
        # Debugging: Überprüfen der geladenen Transkript-Daten
        st.write(f"Loaded Transcript Data: {text_data}")
        
        st.session_state.data.update({'text': text_data['text'], 'word_count': text_data['word_count'], 'selected_language': selected_language})
        st.session_state.show_language_select = False
        st.rerun()
