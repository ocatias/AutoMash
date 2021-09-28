import sys
import os
from helpers import *
from moviepy.editor import VideoFileClip, concatenate_videoclips


"""
    Creates a mashup, that is cuts together videos so they say the specified words.
    Execute with:
        python src\create_video.py project_name "Text that the video should use"
    Please ensure that the text is actually part of the lexicon (see the created list of words)
"""

# Path to the directory in which the videos will be stored
data_path = "tmp"

# Additonal seconds that will be added after each words
additional_time_at_end_of_words = 0.25

max_n_gram_length = 5


lexicon_name = sys.argv[1] + ".lexicon"
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

snippets_path = [get_snippet_path(data_path, lexicon, word) for word in words]
clips = [VideoFileClip(snippet_path) for snippet_path in snippets_path]
final_clip = concatenate_videoclips(clips, method='compose')
final_clip.write_videofile(sys.argv[1] + ".mp4")
