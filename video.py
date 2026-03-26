import subprocess
import os
from datetime import datetime

def play_video(video_filename):

    video_path = f"bmo-face-audio/{video_filename}.mp4"

    if os.path.exists(video_path):
        print(f"BMO is playing video: {video_path}")
        # omxplayer handles the hardware acceleration on the Pi
        # coded on a mac so originally mpv
        subprocess.run(['mpv','--ontop', '--no-border', '--geometry=480x320', video_path])
    else:
        print(f"Error: Could not find {video_path} at {os.path.abspath(video_path)}")


if __name__ == "__main__":

    print("Testing Video Handler...")
    play_video("GiantLeap")

def play_audio(audio_file):

    audio_path = f"bmo-face-audio/{audio_file}.mp3"


    if os.path.exists(video_path):
        print(f"BMO is playing video: {audio_path}")
        # omxplayer handles the hardware acceleration on the Pi
        subprocess.run(['afplay', audio_path])
    else:
        print(f"Error: Could not find {audio_path} at {os.path.abspath(audio_path)}")
