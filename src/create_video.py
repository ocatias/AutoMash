import sys
import os
from helpers import *
from moviepy.editor import VideoFileClip, concatenate_videoclips


"""
    Creates a mashup, that is cuts together videos so they say the specified words.
    Execute with:
        python src\create_video.py project_name
    Please ensure that the project_name the same project_name used int plan_video.py
"""

# Path to the directory in which the videos will be stored
data_path = "tmp"
# Additonal seconds that will be added after each words
pause_between_phrases = 0.1

fade_in_time = 0
fade_out_time = 0

def read_video_plan(path):
    words, time_before, time_after, pause_after = [], [], [], []
    with open(path) as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace("\n", "")
        entries = line.split("\t")
        words.append(entries[0])
        time_before.append(float(entries[1]))
        time_after.append(float(entries[2]))
        pause_after.append(float(entries[3]))

    return words, time_before, time_after, pause_after


project_name = sys.argv[1]
lexicon = unpickle(os.path.join(data_path, project_name + ".lexicon"))

# Parse video plan
words, time_before, time_after, pause_after = read_video_plan(os.path.join(data_path, project_name + "_video_plan.txt"))
data = zip(words, time_before, time_after, pause_after)

snippets_path = [get_snippet_path(fade_in_time, fade_out_time, data_path, lexicon, words, time_before, time_after, pause_after + pause_between_phrases) for (words, time_before, time_after, pause_after) in data]
clips = [VideoFileClip(snippet_path) for snippet_path in snippets_path]
final_clip = concatenate_videoclips(clips, method='compose')
final_clip.write_videofile(sys.argv[1] + ".mp4")
