"""
    Execute directly from the AutoMash directory
"""

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips

def url_to_id(url):
    """
        Transforms the url of a youtube video to its id
    """
    return url.split("watch?v=")[1]

def get_snippet_path(lexicon, text):
    lexicon_entry = lexicon[text]
    path = lexicon_entry["video_path"]
    start = lexicon_entry["start"]
    end = lexicon_entry["end"]

    output_path = os.path.join(video_path, text + ".mp4")

    if not os.path.exists(output_path):
        video = VideoFileClip(path)
        new = video.subclip(start, end)
        new.write_videofile(output_path, audio_codec='aac')
    return output_path



# Videos to download and use
video_urls = []

# Path to the directory in which the videos will be stored
video_path = "tmp"


if not os.path.isdir(video_path):
    os.mkdir(video_path)

# Download videos
print("Downloading videos")
video_paths = []
for url in video_urls:

    yt = YouTube(url)

    video = yt.streams.first()
    video.download(video_path)

    title = yt.title
    print("\tDownloaded {0}".format(title))
    video_paths.append(os.path.join(video_path, video.default_filename))

# Collect transcripts
lexicon = {}
for i, url in enumerate(video_urls):
    id = url_to_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(id)

    for entry in transcript:
        lexicon[entry["text"]] = {"video_path": video_paths[i], "start": entry["start"], "end": entry["start"] + entry["duration"]}

print(lexicon.keys())

words = []

snippets_path = [get_snippet_path(lexicon, word) for word in words]
clips = [VideoFileClip(snippet_path) for snippet_path in snippets_path]
final_clip = concatenate_videoclips(clips)
final_clip.write_videofile("my_concatenation.mp4")
