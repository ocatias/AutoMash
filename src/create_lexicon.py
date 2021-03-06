import sys
from pytube import YouTube
import os
from helpers import *
import config

"""
    Creates a lexicon of words from a list of youtube videos.
    These words can then be mashed together to create a new video, mashing is done with create_video.py
    Execute this script with:
        python src\create_lexicon.py {project_name} {list_of_youtube_urls}
    For example:
        python src\create_lexicon.py MyProject https://www.youtube.com/watch?v=5te73hfCpuU https://www.youtube.com/watch?v=VMinwf-kRlA
"""

config_dict = config.get_config()

transcription_tool = config_dict["transcription_tool"]
data_path = config_dict["tmp_dir"]
words_per_line = config_dict["words_per_line"]
model_path = config_dict["model_path"]

lexicon_name = sys.argv[1]
video_urls = sys.argv[2:]

# Download videos
print("Downloading videos")
video_paths = []
for url in video_urls:

    yt = YouTube(url)
    video = yt.streams.filter(res="720p").first()
    video_path = os.path.join(data_path, video.default_filename)

    # Download video if it is not yet stored
    if not os.path.isfile(video_path):
        video.download(data_path)
        title = yt.title
        print("\tDownloaded {0}".format(title))

    video_paths.append(video_path)

# Collect transcripts
if transcription_tool == "deepspeech":
    import att_deepspeech
    lexicon, transcript = att_deepspeech.get_lexicon(video_paths, data_path, model_path)
elif transcription_tool == "watson":
    import att_ibm_watson
    lexicon, transcript = att_ibm_watson.get_lexicon(video_paths, data_path)
elif transcription_tool == "vosk":
    import att_vosk
    lexicon, transcript = att_vosk.get_lexicon(video_paths, data_path, model_path)
else:
    raise ValueError("Wrong transcription_tool selected, please select either deepspeech or watson")

# Store lexicon
do_pickle(lexicon, os.path.join(data_path, lexicon_name + ".lexicon"))
print("Stored {0} phrases in the lexicon".format(len(lexicon.keys())))

text_file_path = os.path.join(data_path, lexicon_name + ".txt")
with open(text_file_path, "w") as text_file:
    words = transcript.split(" ")
    while len(words) > 0:
        nr_words_in_this_line = min(words_per_line, len(words))
        words_in_this_line = []
        while nr_words_in_this_line > 0:
            nr_words_in_this_line -= 1
            words_in_this_line.append(words[0])
            del words[0]
        text_file.write(" ".join(words_in_this_line) + "\n")

print("You can find the words in a human readable format at: {0}".format(text_file_path))
