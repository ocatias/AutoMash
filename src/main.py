"""
    Execute directly from the AutoMash directory
"""

import os
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from helpers import *

transcription_tool = "youtube"

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

# Words that the final video should use
words = []

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
if transcription_tool == "youtube":
    import att_youtube
    lexicon = att_youtube.get_lexicon(video_urls, video_paths)
elif transcription_tool == "watson":
    import att_ibm_watson
    lexicon = att_ibm_watson.get_lexicon(video_paths)
else:
    raise ValueError("Wrong transcription_tool selected, please select either youtube or watson")

print(lexicon.keys())

snippets_path = [get_snippet_path(lexicon, word) for word in words]
clips = [VideoFileClip(snippet_path) for snippet_path in snippets_path]
final_clip = concatenate_videoclips(clips)
final_clip.write_videofile("my_concatenation.mp4")
