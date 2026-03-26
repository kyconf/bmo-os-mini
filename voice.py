import subprocess
import os

def test_bmo_laptop(text, model_path):
    # Ensure the model exists
    if not os.path.exists(model_path):
        print(f"Error: Could not find {model_path}")
        return

    print(f"Testing B.MO voice on laptop: '{text}'")


    try:
        # 1. Generate the audio file using Piper
        command = f'echo "{text}" | piper --model {model_path} --output_file test_bmo.wav'
        subprocess.run(command, shell=True, check=True)
        

        if os.name == 'posix':  # Mac or Linux
            play_cmd = "afplay test_bmo.wav" if os.uname().sysname == 'Darwin' else "aplay test_bmo.wav"
        else:  # Windows
            play_cmd = "start test_bmo.wav"
            
        subprocess.run(play_cmd, shell=True)
        print("Success!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test
test_bmo_laptop("Mathematical! I am a human living robot!", "en_US-lessac-medium.onnx")