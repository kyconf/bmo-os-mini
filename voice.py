import subprocess
import os


def test_bmo_laptop(text, model_path):
    if not os.path.exists(model_path):
        return

  
    temp_wav = "bmo_output.wav"

    try:

        clean_text = ", , " + text.strip()
        
        scales = "--length_scale 0.85 --noise_scale 0.75 --noise_w 1.0"

        command = f'echo "{clean_text}" | piper --model {model_path} {scales} --output_file {temp_wav}'
        

        subprocess.run(command, shell=True, check=True)

    
        # 'afplay' on Mac or 'aplay' on Pi
        subprocess.run(f"afplay {temp_wav}", shell=True)

    except Exception as e:
        print(f"BMO Error: {e}")


if __name__ == "__main__":
    test_bmo_laptop("   Yes he is a community hole. Ran through at the most.", "en_US-lessac-medium.onnx")