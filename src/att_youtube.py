"""
            Creates a lexicon via the youtube subtitles function
"""
from youtube_transcript_api import YouTubeTranscriptApi
from helpers import *

def get_lexicon(video_urls, video_paths):
    lexicon = {}
    for i, url in enumerate(video_urls):
        id = url_to_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(id)

        for entry in transcript:
            lexicon[entry["text"]] = {"video_path": video_paths[i], "start": entry["start"], "end": entry["start"] + entry["duration"]}
    return lexicon
