import pickle
import os
from moviepy.editor import *
import re

put_phrase_in_video = True

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

def get_snippet_path(fade_in_time, fade_out_time, video_path, lexicon, text, additional_time_before = 0, additional_time_after = 0, time_to_mute_after = 0):
    lexicon_entry = lexicon[text]
    path = lexicon_entry["video_path"]
    start = lexicon_entry["start"]
    end = lexicon_entry["end"]

    output_path = os.path.join(video_path, "{0}_{1}_{2}_{3}_{4}_{5}.mp4".format(text, additional_time_before, additional_time_after, time_to_mute_after, fade_in_time, fade_out_time))

    if not os.path.exists(output_path):
        video = VideoFileClip(path)

        # Set start and end points
        start = start - additional_time_before - fade_in_time
        if start < 0:
            start = 0

        end_audio = end + additional_time_after + fade_out_time
        end = end + additional_time_after + fade_out_time + time_to_mute_after
        if end > video.duration:
            end = video.duration
        if end_audio > video.duration:
            end_audio = video.duration

        video_for_audio = video.subclip(start, end_audio)
        video = video.subclip(start, end)

        # Split the audio into unmuted and muted parts and overwrite original audio
        if end > end_audio:
            audioclip_unmuted = video_for_audio.audio
            if fade_in_time > 0:
                audioclip_unmuted = audioclip_unmuted.audio_fadein(fade_in_time)
            if fade_out_time > 0:
                audioclip_unmuted = audioclip_unmuted.audio_fadeout(fade_out_time)

            empty_sound = lambda t: 0
            audioclip_muted = AudioClip(empty_sound, duration= end - end_audio)
            audioclip = concatenate_audioclips([audioclip_unmuted, audioclip_muted])
            video.audio = audioclip

        # Add the phrase as text to the video

        if put_phrase_in_video:
            txt_clip = TextClip(text, fontsize = 50, color = 'red')
            txt_clip = txt_clip.set_pos('bottom').set_duration(end - start)
            video = CompositeVideoClip([video, txt_clip])

        video.write_videofile(output_path, audio_codec='aac')
    return output_path

def format_string(input):
    """
        Format a string so that it can be represented in a uniform way
    """
    # Transform to lower case
    input = input.lower().strip()

    # Only allow characters and the apostrophe
    regex = re.compile('[^a-zA-Z\' ,.;]')
    input = regex.sub('', input)

    return input

def list_of_dict_to_dict_of_lists(list_of_dicts):
    return {k: [dic[k] for dic in list_of_dicts] for k in list_of_dicts[0]}
