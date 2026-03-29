import subprocess
import os
from datetime import datetime

def play_video(video_filename):
    video_path = f"bmo-face-audio/{video_filename}.mp4"

    if os.path.exists(video_path):
        print(f"BMO is playing: {video_filename}")
        
        # '--screen-speed-hz=60' helps with sync
        # '--window-maximized=no' prevents it from filling the whole screen
        # '--geometry=50%:50%' tells mpv to center itself exactly
        cmd = [
            'mpv', 
            '--ontop', 
            '--no-border', 
            '--geometry=480x320+50%+50%', # The 50%+50% is the 'Center' command
            '--cursor-autohide=always',
            video_path
        ]
        
        # Run and wait for it to finish
        subprocess.run(cmd)
    else:
        print(f"Error: {video_path} not found.")


if __name__ == "__main__":

    print("Testing vid...")
    play_video("GiantLeap")

def play_audio(audio_file):

    audio_path = f"bmo-face-audio/{audio_file}.mp3"


    if os.path.exists(video_path):
        print(f"BMO is playing video: {audio_path}")
        # omxplayer handles the hardware acceleration on the Pi
        subprocess.run(['afplay', audio_path])
    else:
        print(f"Error: Could not find {audio_path} at {os.path.abspath(audio_path)}")
