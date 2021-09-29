"""
            Creates a lexicon with IBM Watson
"""
import os
import moviepy
import requests
import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from helpers import *

watson_api_keyfile = "watson.key"
max_n_gram_length = 10

def get_credentials():
    f = open(watson_api_keyfile, "r")
    lines = f.read().split("\n")
    url = lines[0]
    apikey = lines[1]
    return url, apikey



def query_watson(video_path, url, apikey, tmp_path):
    # Create audio files
    video = moviepy.editor.VideoFileClip(video_path)
    path_to_audio = os.path.join(tmp_path, "sound.mp3")
    video.audio.write_audiofile(path_to_audio)

    # Get transcript from Watson
    headers = {
        'Content-Type': 'audio/mp3',
    }
    data = open(path_to_audio, 'rb').read()
    response = requests.post(url + '/v1/recognize?timestamps=true', headers=headers, data=data, auth=('apikey', apikey))
    print("Received: {0}".format(response))
    json_data = json.loads(response.text)
    return json_data

def get_lexicon(video_paths, tmp_path):
    lexicon = {}
    url, apikey = get_credentials()
    # Parse each video
    for video_path in video_paths:

        # If we have already queried Watson for this video, load the previos query
        json_path = os.path.splitext(video_path)[0] + "_json.pkle"
        if os.path.isfile(json_path):
            json_data = unpickle(json_path)

        # Otherwise query Watson and store the resulting json
        else:
            json_data = query_watson(video_path, url, apikey, tmp_path)
            do_pickle(json_data, json_path)

        # Put transcript into the lexicon
        for result in json_data["results"]:
            for alternative in result["alternatives"]:
                confidence = alternative["confidence"]

                for n_gram_length in range(1, max_n_gram_length + 1):
                    for idx in range(len(alternative["timestamps"]) + 1 - n_gram_length):
                        entries = alternative["timestamps"][idx:idx+n_gram_length]

                        words = format_string(" ".join([entries[i][0] for i in range(n_gram_length)]))
                        start = entries[0][1]
                        end = entries[-1][2]

                        # Only put new words or words Watson is more confident to be correct into the lexicon
                        if words not in lexicon or (words in lexicon and lexicon[words]["confidence"] < confidence):
                            lexicon[words] = {"video_path": video_path, "start": start, "end": end, "confidence": confidence}

    print(lexicon)
    return lexicon
