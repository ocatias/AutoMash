import sys
from pytube import YouTube
import os
from helpers import *

"""
    Creates a lexicon of words from a list of youtube videos.
    These words can then be mashed together to create a new video, mashing is done with create_video.py
    Execute this script with:
        python src\create_lexicon.py {project_name} {list_of_youtube_urls}
    For example:
        python src\create_lexicon.py MyProject https://www.youtube.com/watch?v=5te73hfCpuU https://www.youtube.com/watch?v=VMinwf-kRlA
"""


transcription_tool = "watson"

# Path to the directory in which the videos will be stored
data_path = "tmp"

# Number of words in a line of the readble lexicon
words_per_line = 10

lexicon_name = sys.argv[1]
video_urls = sys.argv[2:]

# Download videos
print("Downloading videos")
video_paths = []
for url in video_urls:

    yt = YouTube(url)

    video = yt.streams.first()
    video.download(data_path)

    title = yt.title
    print("\tDownloaded {0}".format(title))
    video_paths.append(os.path.join(data_path, video.default_filename))

# Collect transcripts
if transcription_tool == "youtube":
    import att_youtube
    lexicon = att_youtube.get_lexicon(video_urls, video_paths)
elif transcription_tool == "watson":
    import att_ibm_watson
    lexicon = att_ibm_watson.get_lexicon(video_paths, data_path)
else:
    raise ValueError("Wrong transcription_tool selected, please select either youtube or watson")

# Store lexicon
do_pickle(lexicon, os.path.join(data_path, lexicon_name + ".lexicon"))
print("Stored {0} words in the lexicon".format(len(lexicon.keys())))

text_file_path = os.path.join(data_path, lexicon_name + ".txt")
with open(text_file_path, "w") as text_file:
    words = list(lexicon.keys())
    lines = []
    for i in range(0, len(words), words_per_line):
        lines.append(", ".join(words[i:i + words_per_line]))

    text_file.write("\n".join(lines))

print("You can find the words in a human readable format at: {0}".format(text_file_path))
