"""
            Creates a lexicon with Vosk
"""
import os
import moviepy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from helpers import *
import json
import numpy as np
from vosk import Model, KaldiRecognizer
import wave
import soundfile as sf
import librosa
import config

def use_vosk(video_path, tmp_path, model):
    # Create audio files
    video = moviepy.editor.VideoFileClip(video_path)
    path_to_audio = os.path.join(tmp_path, "sound.wav")
    path_to_audio2 = os.path.join(tmp_path, "sound_transformed.wav")
    video.audio.write_audiofile(path_to_audio)

    # Transform wave file to 16 bit, 16 kHz, mono
    x, sr = librosa.load(path_to_audio, sr=44100)
    sf.write(path_to_audio2, x, 44100, 'PCM_16')

    wf = wave.open(path_to_audio2, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    json_temp = []
    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            json_temp.append(json.loads(rec.Result()))

    json_data = []
    for result in json_temp:
        json_data += result["result"]
    print(json_data)
    return json_data

def get_lexicon(video_paths, tmp_path, model_path):
    print("ATT VBOSK")
    config_dict = config.get_config()
    model = Model(model_path)
    lexicon = {}
    transcript = ""
    # Parse each video
    for video_path in video_paths:

        # If we have already parsed this video with deepspeech then load the previous result
        json_path = os.path.splitext(video_path)[0] + "_vosk_json.pkle"
        if os.path.isfile(json_path):
            json_data = unpickle(json_path)
        # Otherwise use vosk
        else:
            json_data = use_vosk(video_path, tmp_path, model)
            do_pickle(json_data, json_path)

    # Put n-grams into the lexicon and create a transcript
    for idx, word in enumerate(json_data):
        confidence = word["conf"]
        transcript += format_string(word["word"]) + " "

        for n_gram_length in range(1, min(config_dict["max_n_gram_length"] + 1, len(json_data) - idx)):
            entries = json_data[idx:idx+n_gram_length]

            words = format_string(" ".join([entries[i]["word"] for i in range(n_gram_length)]))
            start = entries[0]["start"]
            end = entries[-1]["end"]

            # Only put new words or words Watson is more confident to be correct into the lexicon
            if words not in lexicon or (words in lexicon and lexicon[words]["confidence"] < confidence):
                lexicon[words] = {"video_path": video_path, "start": start, "end": end, "confidence": confidence}

    return lexicon, transcript
