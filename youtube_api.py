import re
import uuid
from youtube_transcript_api import (YouTubeTranscriptApi, VideoUnavailable,
                                   TranscriptsDisabled, NoTranscriptFound)
import streamlit as st

def extract_video_id(url):
    # Combine patterns into a single, more efficient regex
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
        return []

def load_youtube_transcript(video_id, languages=['en']):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        transcript = ' '.join([t['text'] for t in transcript_list])
        word_count = len(transcript.split())
        return transcript, word_count
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        return {"error": str(e), "success": False} # Return error details

def process_youtube_input(youtube_input):
    video_id = extract_video_id(youtube_input)
    if not video_id:
        st.error("Please enter a valid YouTube URL or ID.")
        return None

    languages = list_available_transcripts(video_id)
    if not languages:
        st.error("No available transcripts found for this video.")
        return None 

    unique_key = f"language_select_{uuid.uuid4()}"
    selected_language = st.selectbox("Select Language", languages, key=unique_key)

    if selected_language: 
        return {
            "video_id": video_id,
            "selected_language": selected_language 
        } # Store only essential information in session state
    else:
        st.info("Please select a language to load the transcript.")
        return None
