import sys
import os
from helpers import *
from moviepy.editor import VideoFileClip, concatenate_videoclips

"""
    After creating a video this script can be used to plan the video.
    It will output a text file that allows you to manipulate the length of sounds.
    Execute with:
        python src\plan_video.py project_name "Text that the video should use"
    Please ensure that the text is actually part of the lexicon (see the created list of words)
    and that project_name is the same project_name as selected in create_lexicon.py
"""

# Path to the directory in which the videos will be stored
data_path = "tmp"

# Additonal seconds that will be added after each words
additional_time_at_end_of_words = 0.25

max_n_gram_length = 5


project_name = sys.argv[1]
lexicon_name = project_name + ".lexicon"
text = sys.argv[2].split(" ")
words_unparsed = [format_string(x) for x in text if x != ""]

lexicon = unpickle(os.path.join(data_path, lexicon_name))

# Add aditional time
for key in lexicon.keys():
    lexicon[key]["end"] += additional_time_at_end_of_words

# Try to greedily get the biggest possible n-grams from the word list
words = []
while len(words_unparsed) > 0:
    for n in range(max_n_gram_length, 0, -1):
        n_gram = " ".join(words_unparsed[0:n])
        if n_gram in lexicon.keys():
            words.append(n_gram)
            del words_unparsed[:n]
            break

text_file_path = os.path.join(data_path, project_name + "_video_plan.txt")
with open(text_file_path, "w") as text_file:
    for word in words:
        text_file.write(word +"\t0\t0\n")

print("Created the video plan, you can read and change it: {0}".format(text_file_path))
