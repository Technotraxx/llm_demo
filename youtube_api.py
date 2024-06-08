import re
import uuid
from youtube_transcript_api import (YouTubeTranscriptApi, VideoUnavailable,
                                   TranscriptsDisabled, NoTranscriptFound)
import streamlit as st

def extract_video_id(url):
    print("Extracting video ID...")  # Debug: Check if function is called
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|)([a-zA-Z0-9_-]{11})'
    match = re.match(pattern, url)
    if match:
        video_id = match.group(1)
        print(f"Found video ID: {video_id}") # Debug: Print extracted ID
        return video_id
    else:
        print("No video ID found.") # Debug: Indicate no match found
        return None

def list_available_transcripts(video_id):
    print(f"Listing transcripts for video ID: {video_id}") # Debug
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = [transcript.language_code for transcript in transcript_list]
        print(f"Available languages: {languages}") # Debug: Show found languages
        return languages
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"Error listing transcripts: {e}") # Debug: Print the error
        st.error(f"Error: {str(e)}") # Show error to the user
        return []

def load_youtube_transcript(video_id, selected_language):
    print(f"Loading transcript for video ID: {video_id}, Language: {selected_language}")
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language])
        transcript = ' '.join([t['text'] for t in transcript_list])
        word_count = len(transcript.split())
        print(f"Transcript loaded successfully. Word count: {word_count}")
        return {
            "text": transcript,
            "word_count": word_count
        }
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        print(f"Error loading transcript: {e}") # Debug: Print the error
        st.error(f"Error: {str(e)}") # Show error to the user
        return {"error": str(e), "success": False}

def process_youtube_input(youtube_input):
    print("Processing YouTube input...") 
    video_id = extract_video_id(youtube_input)
    if not video_id:
        return None

    languages = list_available_transcripts(video_id)
    if not languages:
        return None
    
    print("Creating language selection box...") # Debug
    unique_key = f"language_select_{uuid.uuid4()}"
    selected_language = st.selectbox("Select Language", languages, key=unique_key)
    print(f"Selected language: {selected_language}") # Debug

    if selected_language:
        transcript_data = load_youtube_transcript(video_id, selected_language)
        if "error" in transcript_data:
            return None
        else:
            print("Returning processed YouTube data...") # Debug
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
            text, word_count = load_youtube_transcript(result['video_id'], result['languages'][0])
            st.session_state.data.update({'text': text, 'word_count': word_count})
    else:
        st.warning("Failed to process YouTube input.")

def handle_language_selection():
    if st.session_state.get('show_language_select', False):
        st.write("Select Transcript Language:")
        selected_language = st.selectbox("Select Language", st.session_state.data['languages'])
        text, word_count = load_youtube_transcript(st.session_state.data['video_id'], selected_language)
        st.session_state.data.update({'text': text, 'word_count': word_count, 'selected_language': selected_language})
        st.session_state.show_language_select = False
        st.rerun()
