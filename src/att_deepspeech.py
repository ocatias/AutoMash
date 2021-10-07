"""
            Creates a lexicon with Mozilla DeepSpeech
"""
import os
import moviepy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from helpers import *
import subprocess
import soundfile as sf
import librosa
import deep_speech_client
import json
import numpy as np

watson_api_keyfile = "watson.key"
max_n_gram_length = 10
model_path = "deepspeech-0.9.3-models.pbmm"

def use_deepspeech(video_path, tmp_path):
    print(video_path)

    # Create audio files
    video = moviepy.editor.VideoFileClip(video_path)
    path_to_audio = os.path.join(tmp_path, "sound.wav")
    path_to_audio2 = os.path.join(tmp_path, "sound_transformed.wav")
    video.audio.write_audiofile(path_to_audio)

    # Transform wave file to 16 bit, 16 kHz, mono
    x, sr = librosa.load(path_to_audio, sr=44100)
    y = librosa.resample(x, sr, 16000)
    sf.write(path_to_audio2, y, 16000, 'PCM_16')

    response = deep_speech_client.inference(model_path, path_to_audio2)
    json_data = json.loads(response)
    # print("json_data", json_data)
    return json_data

def get_lexicon(video_paths, tmp_path):
    lexicon = {}
    transcript = ""
    # Parse each video
    for video_path in video_paths:

        # If we have already parsed this video with deepspeech then load the previous result
        json_path = os.path.splitext(video_path)[0] + "_deepspeech_json.pkle"
        if os.path.isfile(json_path):
            json_data = unpickle(json_path)
        # Otherwise use deepspeech
        else:
            json_data = use_deepspeech(video_path, tmp_path)
            do_pickle(json_data, json_path)

        confidences = [x["confidence"] for x in json_data["transcripts"]]
        idx = np.argmax(confidences)

        # Put n-grams into the lexicon and create a transcript
        alternative = json_data["transcripts"][idx]
        confidence = confidences[idx]
        transcript += " ".join([x["word"] for x in alternative["words"]]) + "\n "

        for n_gram_length in range(1, max_n_gram_length + 1):
            for idx in range(len(alternative["words"]) + 1 - n_gram_length):
                entries = alternative["words"][idx:idx+n_gram_length]

                words = format_string(" ".join([entries[i]["word"] for i in range(n_gram_length)]))
                start = entries[0]["start_time"]
                end = start + sum([entry["duration"] for entry in entries])

                # Only put new words or words Watson is more confident to be correct into the lexicon
                if words not in lexicon or (words in lexicon and lexicon[words]["confidence"] < confidence):
                    lexicon[words] = {"video_path": video_path, "start": start, "end": end, "confidence": confidence}

    return lexicon, transcript
