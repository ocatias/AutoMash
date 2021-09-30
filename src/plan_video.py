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

pause_after_comma = 0.1
pause_after_dot = 0.2
pause_after_semicolon = 0.15

max_n_gram_length = 5


project_name = sys.argv[1]
lexicon_name = project_name + ".lexicon"
text = sys.argv[2].split(" ")
words_unparsed_original_formatting = [x for x in text if x != ""]
words_unparsed = [format_string(x) for x in text if x != ""]

lexicon = unpickle(os.path.join(data_path, lexicon_name))

# Try to greedily get the biggest possible n-grams from the word list
words = []
words_original_formatting = []
mute_time_after_word = []
while len(words_unparsed) > 0:
    for n in range(max_n_gram_length, -1, -1):
        # Exit if we could not find a one word phrase in our lexicon
        if n == 0:
            raise ValueError("Could not find {0} in the lexicon".format(words_unparsed[0]))

        n_gram = " ".join(words_unparsed[0:n])
        n_gram_original_formatting = " ".join(words_unparsed_original_formatting[0:n])
        print(n_gram_original_formatting)

        n_gram_cleared = n_gram.replace(",", "").replace(".", "").replace(";", "")
        if n_gram_cleared in lexicon.keys():
            words.append(n_gram_cleared)
            words_original_formatting.append(n_gram_original_formatting)

            # Add pause if the n_gram ends on . or ,
            pause = 0
            while(n_gram[-1] in [".", ",", ";"]):
                if n_gram[-1] == ".":
                    pause += pause_after_dot
                elif n_gram[-1] == ",":
                    pause += pause_after_comma
                elif n_gram[-1] == ";":
                    pause += pause_after_semicolon
                n_gram = n_gram[:-1]

            mute_time_after_word.append(pause)
            del words_unparsed[:n]
            del words_unparsed_original_formatting[:n]
            break

text_file_path = os.path.join(data_path, project_name + "_video_plan.txt")
with open(text_file_path, "w") as text_file:
    for word, pause in zip(words_original_formatting, mute_time_after_word):
        text_file.write(word +"\t0\t0\t{0}\n".format(pause))

print("Created the video plan, you can read and change it: {0}".format(text_file_path))
