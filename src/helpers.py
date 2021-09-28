import pickle
import os
from moviepy.editor import VideoFileClip
import re

def url_to_id(url):
    """
        Transforms the url of a youtube video to its id
    """
    return url.split("watch?v=")[1]

def do_pickle(data, path):
    with open(path, 'wb') as file:
        pickle.dump(data, file)
        file.close()

def unpickle(path):
    data = None
    with open(path, 'rb') as file:
        data = pickle.load(file)
        file.close()
    return data

def get_snippet_path(video_path, lexicon, text):
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

def format_string(input):
    """
        Format a string so that it can be represented in a uniform way
    """
    # Transform to lower case
    input = input.lower()

    # Only allow characters and the apostrophe
    regex = re.compile('[^a-zA-Z\' ]')
    input = regex.sub('', input)

    return input

def list_of_dict_to_dict_of_lists(list_of_dicts):
    return {k: [dic[k] for dic in list_of_dicts] for k in list_of_dicts[0]}
