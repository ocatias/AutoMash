"""
            Creates a lexicon with IBM Watson
"""
import os
import moviepy
import requests
import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips

watson_api_keyfile = "watson.key"

def get_credentials():
    f = open(watson_api_keyfile, "r")
    lines = f.read().split("\n")
    url = lines[0]
    apikey = lines[1]
    return url, apikey

def get_lexicon(video_paths, tmp_path):
    lexicon = {}
    url, apikey = get_credentials()
    # Parse each video
    for path in video_paths:

        # Create audio files
        clip = moviepy.editor.VideoFileClip(path)
        path_to_audio = os.path.join(tmp_path, "sound.mp3")
        clip.audio.write_audiofile(path_to_audio)

        # Get transcript from Watson
        headers = {
            'Content-Type': 'audio/mp3',
        }
        data = open(path_to_audio, 'rb').read()
        response = requests.post(url + '/v1/recognize?timestamps=true', headers=headers, data=data, auth=('apikey', apikey))
        print("Received: {0}".format(response))
        json_data = json.loads(response.text)
        # print(json_data)

        # Put transcript into the lexicon
        for result in json_data["results"]:
            for alternative in result["alternatives"]:
                confidence = alternative["confidence"]
                for entry in alternative["timestamps"]:
                    word = entry[0].lower().replace(" ", "")
                    start = entry[1]
                    end = entry[2]

                    # Only put new words or words Watson is more confident to be correct into the lexicon
                    if word not in lexicon or (word in lexicon and lexicon[word]["confidence"] < confidence):
                        lexicon[word] = {"video_path": path, "start": start, "end": end, "confidence": confidence}

    print(lexicon)
    return lexicon
