import re
import uuid
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable, TranscriptsDisabled, NoTranscriptFound

def load_youtube_transcript(video_id, languages=['en']):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        transcript = ' '.join([t['text'] for t in transcript_list])
        word_count = len(transcript.split())
        return transcript, word_count
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        return f"Error: {str(e)}", 0

def list_available_transcripts(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        languages = [transcript.language_code for transcript in transcript_list]
        return languages
    except (VideoUnavailable, TranscriptsDisabled, NoTranscriptFound) as e:
        return []

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL.

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The video ID, or None if the URL is invalid.
    """

    # Use a single regex to cover all common YouTube URL formats
    pattern = r'^(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|)([^?&/]+)'
    match = re.match(pattern, url)

    if match:
        return match.group(1)
    else:
        return None
